# /backend/app/routers/analyze.py

from fastapi import APIRouter, HTTPException, Depends, UploadFile, File
import logging

# Modelos Pydantic para a estrutura dos dados
from app.models.artwork_analysis import ArtworkAnalysisRequest, ArtworkAnalysisResponse

# Serviços que contêm a lógica de negócio
from app.services.groq_service import get_groq_service, GroqService
from app.services.database_service import get_database_service, DatabaseService

# Funções utilitárias e configurações
from app.core.config import settings
from app.core.utils import generate_image_hash

# Configuração do logger para este ficheiro
logger = logging.getLogger(__name__)

# Criação do router que será incluído na aplicação principal
router = APIRouter()


@router.post("/analise-por-nome", response_model=ArtworkAnalysisResponse, tags=["Analysis"])
async def analyze_artwork_by_name(
    request: ArtworkAnalysisRequest,
    db_service: DatabaseService = Depends(get_database_service),
    groq_service: GroqService = Depends(get_groq_service)
):
    """
    Analisa uma obra de arte pelo nome, verificando primeiro o cache.
    """
    try:
        artwork_name = request.artwork_name.strip()
        if not artwork_name:
            raise HTTPException(status_code=400, detail="O nome da obra de arte é obrigatório.")
        
        logger.info(f"🔍 Recebida requisição para analisar por texto: {artwork_name}")
        
        # 1. Verificar se a análise já existe no cache pelo nome
        cached_analysis = await db_service.get_analysis_by_name(artwork_name)
        if cached_analysis:
            logger.info(f"✅ Análise encontrada em cache para: {artwork_name}")
            return cached_analysis
        
        # 2. Se não estiver no cache, gerar nova análise com a IA
        logger.info(f"🤖 Gerando nova análise com Groq para: {artwork_name}")
        analysis_data = await groq_service.analyze_artwork(artwork_name)
        
        # 3. Salvar a nova análise na base de dados
        saved_analysis = await db_service.save_analysis(analysis_data)
        logger.info(f"💾 Análise para '{artwork_name}' salva na base de dados.")
        
        return saved_analysis
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ Erro na análise da obra {request.artwork_name}: {str(e)}")
        raise HTTPException(status_code=500, detail="Ocorreu um erro interno ao processar a sua solicitação.")


@router.post("/analise-por-imagem", response_model=ArtworkAnalysisResponse, tags=["Analysis"])
async def analyze_artwork_by_image(
    file: UploadFile = File(..., description="Ficheiro de imagem da obra de arte"),
    db_service: DatabaseService = Depends(get_database_service),
    groq_service: GroqService = Depends(get_groq_service)
):
    """
    Analisa uma obra de arte a partir de uma imagem, com um fluxo de cache inteligente de múltiplos passos.
    """
    # 1. Validação do ficheiro
    if not file.content_type in settings.ALLOWED_IMAGE_TYPES:
        raise HTTPException(
            status_code=415, 
            detail=f"Tipo de ficheiro não suportado. Use um dos seguintes: {', '.join(settings.ALLOWED_IMAGE_TYPES)}"
        )

    image_data = await file.read()
    if len(image_data) > settings.MAX_FILE_SIZE:
        raise HTTPException(
            status_code=413,
            detail=f"Ficheiro muito grande. O tamanho máximo é {settings.MAX_FILE_SIZE // (1024*1024)}MB."
        )

    try:
        # --- FLUXO DE CACHE INTELIGENTE ---

        # ETAPA 1: Verificar cache pelo HASH da imagem (ficheiro idêntico)
        image_hash = generate_image_hash(image_data)
        cached_analysis = await db_service.get_analysis_by_image_hash(image_hash)
        if cached_analysis:
            logger.info(f"✅ Análise encontrada em cache pelo HASH da imagem.")
            return cached_analysis

        # ETAPA 2: Se não encontrou pelo hash, IDENTIFICAR a obra via IA
        logger.info("🔍 Hash não encontrado. A tentar identificar a obra na imagem...")
        identification_result = await groq_service.identify_artwork_from_image(image_data)
        
        if identification_result:
            artwork_name = identification_result.get("artwork_name")
            
            # ETAPA 3: Verificar cache pelo NOME da obra identificada
            cached_by_name = await db_service.get_analysis_by_name(artwork_name)
            if cached_by_name:
                logger.info(f"✅ Obra identificada como '{artwork_name}'. Análise encontrada em cache pelo nome.")
                # Opcional: Poderíamos associar o hash da nova imagem à análise existente
                # mas por agora, apenas retornamos a análise encontrada para economizar uma escrita na DB.
                return cached_by_name

        # ETAPA 4: Se chegou até aqui, é uma obra nova. Fazer a ANÁLISE COMPLETA.
        logger.info(f"🤖 Nenhuma análise em cache. A gerar nova análise completa para a imagem...")
        analysis_data = await groq_service.analyze_artwork_from_image(image_data)
        
        # Se a IA identificou um nome na etapa de identificação, usamos esse nome
        # para garantir consistência.
        if identification_result and identification_result.get("artwork_name"):
             analysis_data["artwork_name"] = identification_result.get("artwork_name")
             
        # Salvar a nova análise na base de dados, associando o hash da imagem
        saved_analysis = await db_service.save_analysis(analysis_data, image_hash=image_hash)
        logger.info(f"💾 Nova análise de imagem salva na base de dados.")
        
        return saved_analysis

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ Erro crítico na análise da imagem: {str(e)}")
        raise HTTPException(status_code=500, detail="Ocorreu um erro interno ao processar a imagem.")