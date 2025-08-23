# /backend/app/routers/analyze.py

from fastapi import APIRouter, HTTPException, Depends, UploadFile, File
import logging
import httpx # Importe o httpx para fazer as requisições
from app.models.artwork_analysis import ArtworkAnalysisRequest, ArtworkAnalysisResponse
from app.services.groq_service import get_groq_service, GroqService
from app.services.database_service import get_database_service, DatabaseService
from app.core.config import settings
from app.core.utils import generate_image_hash

logger = logging.getLogger(__name__)
router = APIRouter()

async def find_valid_image_url(artwork_name: str, artist: str | None) -> str | None:
    """
    Busca URLs de imagens e verifica se são válidos antes de retornar o primeiro
    que encontrar.
    """
    # AQUI É ONDE VOCÊ PRECISARÁ INTEGRAR O SEU SERVIÇO DE BUSCA DE IMAGENS.
    # Esta lista de exemplo simula os URLs que uma API de busca retornaria.
    # Exemplo de URLs que poderiam vir de uma API de busca:
    potential_urls = [
        # Coloque aqui as chamadas à sua API de busca para obter URLs
        # Por exemplo: google_search(f'{artwork_name} {artist} high quality image')
        f"https://example.com/images/{artwork_name.replace(' ', '_')}.jpg",
        "https://www.wikipedia.org/some_other_image.png",
        "https://broken-link.com/image.jpg"
    ]
    
    # A sua lógica de busca real substituiria esta lista.

    async with httpx.AsyncClient(timeout=10) as client:
        for url in potential_urls:
            try:
                # Tenta fazer uma requisição HEAD para verificar se a URL é válida
                response = await client.head(url, follow_redirects=True)
                if response.status_code == 200 and response.headers.get('content-type', '').startswith('image'):
                    logger.info(f"URL de imagem válida encontrada: {url}")
                    return url
            except httpx.RequestError as e:
                logger.warning(f"Erro ao verificar URL {url}: {e}")
                continue # Continua para a próxima URL em caso de erro

    logger.warning("Nenhum URL de imagem válido foi encontrado após todas as tentativas.")
    return None

@router.post("/analise-por-nome", response_model=ArtworkAnalysisResponse, tags=["Analysis"])
async def analyze_artwork_by_name(
    request: ArtworkAnalysisRequest,
    db_service: DatabaseService = Depends(get_database_service),
    groq_service: GroqService = Depends(get_groq_service)
):
    try:
        artwork_name = request.artwork_name.strip()
        if not artwork_name:
            raise HTTPException(status_code=400, detail="O nome da obra de arte é obrigatório.")
        
        cached_analysis = await db_service.get_analysis_by_name(artwork_name)
        if cached_analysis:
            return cached_analysis
        
        # 1. Obter a análise textual da IA
        analysis_data = await groq_service.analyze_artwork(artwork_name)
        
        # 2. Usar o nome e o artista para encontrar e validar um URL de imagem
        confirmed_artwork_name = analysis_data.get("artwork_name")
        artist = analysis_data.get("artist")
        image_url = await find_valid_image_url(confirmed_artwork_name, artist)
        
        # 3. Adicionar o URL encontrado à análise
        analysis_data["image_url"] = image_url
        
        saved_analysis = await db_service.save_analysis(analysis_data)
        return saved_analysis
        
    except Exception as e:
        logger.error(f"Erro na análise da obra {request.artwork_name}: {str(e)}")
        raise HTTPException(status_code=500, detail="Ocorreu um erro interno ao processar a sua solicitação.")

@router.post("/analise-por-imagem", response_model=ArtworkAnalysisResponse, tags=["Analysis"])
async def analyze_artwork_by_image(
    file: UploadFile = File(...),
    db_service: DatabaseService = Depends(get_database_service),
    groq_service: GroqService = Depends(get_groq_service)
):
    # ... (código de validação e cache permanece o mesmo)
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
        image_hash = generate_image_hash(image_data)
        cached_analysis = await db_service.get_analysis_by_image_hash(image_hash)
        if cached_analysis:
            logger.info(f"✅ Análise encontrada em cache pelo HASH da imagem.")
            return cached_analysis

        logger.info("🔍 Hash não encontrado. A tentar identificar a obra na imagem...")
        identification_result = await groq_service.identify_artwork_from_image(image_data)
        
        if identification_result:
            artwork_name = identification_result.get("artwork_name")
            cached_by_name = await db_service.get_analysis_by_name(artwork_name)
            if cached_by_name:
                logger.info(f"✅ Obra identificada como '{artwork_name}'. Análise encontrada em cache pelo nome.")
                return cached_by_name

        logger.info(f"🤖 Nenhuma análise em cache. A gerar nova análise completa para a imagem...")
        analysis_data = await groq_service.analyze_artwork_from_image(image_data)
        
        if identification_result and identification_result.get("artwork_name"):
             analysis_data["artwork_name"] = identification_result.get("artwork_name")
             
        # Usar o nome da obra para encontrar uma imagem válida para a análise
        confirmed_artwork_name = analysis_data.get("artwork_name")
        artist = analysis_data.get("artist")
        image_url = await find_valid_image_url(confirmed_artwork_name, artist)
        analysis_data["image_url"] = image_url
        
        saved_analysis = await db_service.save_analysis(analysis_data, image_hash=image_hash)
        logger.info(f"💾 Nova análise de imagem salva na base de dados.")
        
        return saved_analysis

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ Erro crítico na análise da imagem: {str(e)}")
        raise HTTPException(status_code=500, detail="Ocorreu um erro interno ao processar a imagem.")