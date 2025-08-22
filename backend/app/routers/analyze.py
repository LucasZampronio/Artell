from fastapi import APIRouter, HTTPException, UploadFile, File, Form
from fastapi.responses import JSONResponse
from typing import Optional
import logging
from app.services.ai_service import ai_service
from app.services.analysis_service import analysis_service
from app.models.analysis import AnalysisRequest, AnalysisResponse
from app.core.config import settings

logger = logging.getLogger(__name__)
router = APIRouter()

@router.post("/image", response_model=AnalysisResponse)
async def analyze_artwork_image(
    file: UploadFile = File(..., description="Imagem da obra de arte")
):
    """
    Analisa uma obra de arte através de uma imagem.
    
    - **file**: Imagem da obra de arte (JPEG, PNG, WebP)
    - **max_size**: 10MB
    """
    try:
        # Validação do arquivo
        if not file.content_type in settings.ALLOWED_IMAGE_TYPES:
            raise HTTPException(
                status_code=400, 
                detail=f"Tipo de arquivo não suportado. Tipos permitidos: {settings.ALLOWED_IMAGE_TYPES}"
            )
        
        # Lê o arquivo
        image_data = await file.read()
        
        if len(image_data) > settings.MAX_FILE_SIZE:
            raise HTTPException(
                status_code=400,
                detail=f"Arquivo muito grande. Tamanho máximo: {settings.MAX_FILE_SIZE // (1024*1024)}MB"
            )
        
        # Verifica se já existe análise para esta imagem
        image_hash = ai_service._generate_image_hash(image_data)
        existing_analysis = await analysis_service.get_analysis_by_image_hash(image_hash)
        
        if existing_analysis:
            logger.info(f"Análise encontrada em cache para hash: {image_hash}")
            return existing_analysis
        
        # Realiza a análise com IA
        logger.info("Iniciando análise de imagem com IA...")
        analysis_create = await ai_service.analyze_artwork_image(image_data)
        
        # Salva a análise na base de dados
        analysis_response = await analysis_service.create_analysis(analysis_create)
        
        logger.info(f"Análise de imagem concluída: {analysis_response.artwork_name}")
        return analysis_response
        
    except Exception as e:
        logger.error(f"Erro na análise de imagem: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/text", response_model=AnalysisResponse)
async def analyze_artwork_text(
    request: AnalysisRequest
):
    """
    Analisa uma obra de arte através do nome.
    
    - **artwork_name**: Nome da obra de arte
    """
    try:
        if not request.artwork_name or request.artwork_name.strip() == "":
            raise HTTPException(
                status_code=400,
                detail="Nome da obra de arte é obrigatório"
            )
        
        # Verifica se já existe análise para este nome
        existing_analysis = await analysis_service.get_analysis_by_name(request.artwork_name)
        
        if existing_analysis:
            logger.info(f"Análise encontrada em cache para: {request.artwork_name}")
            return existing_analysis
        
        # Realiza a análise com IA
        logger.info(f"Iniciando análise por texto para: {request.artwork_name}")
        analysis_create = await ai_service.analyze_artwork_text(request.artwork_name)
        
        # Salva a análise na base de dados
        analysis_response = await analysis_service.create_analysis(analysis_create)
        
        logger.info(f"Análise por texto concluída: {analysis_response.artwork_name}")
        return analysis_response
        
    except Exception as e:
        logger.error(f"Erro na análise por texto: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/upload", response_model=AnalysisResponse)
async def upload_and_analyze(
    file: UploadFile = File(..., description="Imagem da obra de arte"),
    artwork_name: Optional[str] = Form(None, description="Nome opcional da obra")
):
    """
    Endpoint alternativo para upload e análise de imagem.
    Permite especificar um nome opcional para a obra.
    """
    try:
        # Validação do arquivo
        if not file.content_type in settings.ALLOWED_IMAGE_TYPES:
            raise HTTPException(
                status_code=400, 
                detail=f"Tipo de arquivo não suportado. Tipos permitidos: {settings.ALLOWED_IMAGE_TYPES}"
            )
        
        # Lê o arquivo
        image_data = await file.read()
        
        if len(image_data) > settings.MAX_FILE_SIZE:
            raise HTTPException(
                status_code=400,
                detail=f"Arquivo muito grande. Tamanho máximo: {settings.MAX_FILE_SIZE // (1024*1024)}MB"
            )
        
        # Verifica cache
        image_hash = ai_service._generate_image_hash(image_data)
        existing_analysis = await analysis_service.get_analysis_by_image_hash(image_hash)
        
        if existing_analysis:
            logger.info(f"Análise encontrada em cache para hash: {image_hash}")
            return existing_analysis
        
        # Realiza análise
        analysis_create = await ai_service.analyze_artwork_image(image_data)
        
        # Se foi fornecido um nome, sobrescreve
        if artwork_name:
            analysis_create.artwork_name = artwork_name
        
        # Salva na base de dados
        analysis_response = await analysis_service.create_analysis(analysis_create)
        
        logger.info(f"Análise de upload concluída: {analysis_response.artwork_name}")
        return analysis_response
        
    except Exception as e:
        logger.error(f"Erro no upload e análise: {e}")
        raise HTTPException(status_code=500, detail=str(e))
