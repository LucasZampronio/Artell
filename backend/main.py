# /backend/main.py

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from dotenv import load_dotenv
import logging
import asyncio

# Importar modelos e serviços
from app.models.artwork_analysis import ArtworkAnalysisRequest, ArtworkAnalysisResponse
from app.services.groq_service import groq_service
from app.services.database_service import database_service
from app.core.config import settings

# ✨ 1. IMPORTAR O ROUTER DE ANALYSES ✨
from app.routers.analyses import router as analyses_router

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Carregar variáveis de ambiente
load_dotenv()

# Criar aplicação FastAPI
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="API para análise de obras de arte usando IA (Groq)",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configuração CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✨ 2. INCLUIR O ROUTER NA APLICAÇÃO ✨
app.include_router(analyses_router, prefix="/analyses", tags=["Analyses"])


# Eventos de startup e shutdown
@app.on_event("startup")
async def startup_event():
    """Evento executado na inicialização da aplicação"""
    try:
        logger.info("🚀 Iniciando aplicação Artell com Groq...")
        await database_service.connect()
        logger.info("✅ Aplicação iniciada com sucesso!")
    except Exception as e:
        logger.error(f"❌ Erro ao iniciar aplicação: {e}")
        raise e

@app.on_event("shutdown")
async def shutdown_event():
    """Evento executado no encerramento da aplicação"""
    try:
        logger.info("🔄 Encerrando aplicação...")
        await database_service.disconnect()
        logger.info("✅ Aplicação encerrada com sucesso!")
    except Exception as e:
        logger.error(f"❌ Erro ao encerrar aplicação: {e}")

# Endpoints da API (do main.py)

@app.get("/", tags=["Root"])
async def root():
    """Endpoint raiz com informações da API"""
    return {
        "message": "Bem-vindo ao Artell API! 🎨",
        "version": settings.APP_VERSION,
        "docs": "/docs",
    }

@app.get("/health", tags=["Health"])
async def health_check():
    """Endpoint de verificação de saúde da aplicação"""
    return {
        "status": "healthy",
        "service": "Artell API",
        "database": "connected" if database_service.client else "disconnected"
    }

@app.post("/analise-por-nome", response_model=ArtworkAnalysisResponse, tags=["Analysis"])
async def analyze_artwork_by_name(request: ArtworkAnalysisRequest):
    """
    Analisa uma obra de arte pelo nome usando IA (Groq)
    """
    try:
        artwork_name = request.artwork_name.strip()
        if not artwork_name:
            raise HTTPException(status_code=400, detail="Nome da obra de arte é obrigatório")
        
        logger.info(f"🔍 Recebida requisição para analisar: {artwork_name}")
        
        cached_analysis = await database_service.get_analysis_by_name(artwork_name)
        if cached_analysis:
            logger.info(f"✅ Análise encontrada em cache para: {artwork_name}")
            return cached_analysis
        
        logger.info(f"🤖 Gerando nova análise com Groq para: {artwork_name}")
        analysis_data = await groq_service.analyze_artwork(artwork_name)
        
        saved_analysis = await database_service.save_analysis(analysis_data)
        logger.info(f"💾 Análise salva na base de dados: {artwork_name}")
        
        return saved_analysis
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ Erro na análise da obra {request.artwork_name}: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Erro interno do servidor: {str(e)}")

# ... (Os endpoints /analises-recentes e /estatisticas podem ser removidos daqui, pois já existem em analyses.py)

# Executar aplicação se chamado diretamente
if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )