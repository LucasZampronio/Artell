# /backend/main.py

from fastapi import FastAPI, HTTPException, Depends # 1. Adicionar Depends
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from dotenv import load_dotenv
import logging
from app.routers.analyze import router as analyze_router
# 2. Importar os modelos e as FUNÇÕES GETTER dos serviços (não as instâncias globais)
from app.models.artwork_analysis import ArtworkAnalysisRequest, ArtworkAnalysisResponse
from app.services.groq_service import get_groq_service, GroqService
from app.services.database_service import get_database_service, DatabaseService
from app.core.config import settings
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

# Incluir o router de analyses, que já usa Depends
app.include_router(analyze_router, tags=["Analysis"])
app.include_router(analyses_router, prefix="/analyses", tags=["Analyses"])

# 3. Atualizar os eventos de startup e shutdown para usar os getters
@app.on_event("startup")
async def startup_event():
    """Evento executado na inicialização da aplicação"""
    try:
        logger.info("🚀 Iniciando aplicação Artell com Groq...")
        # Obter a instância do serviço e conectar
        db_service = get_database_service()
        await db_service.connect()
        logger.info("✅ Aplicação iniciada com sucesso!")
    except Exception as e:
        logger.error(f"❌ Erro ao iniciar aplicação: {e}")
        raise e

@app.on_event("shutdown")
async def shutdown_event():
    """Evento executado no encerramento da aplicação"""
    try:
        logger.info("🔄 Encerrando aplicação...")
        db_service = get_database_service()
        await db_service.disconnect()
        logger.info("✅ Aplicação encerrada com sucesso!")
    except Exception as e:
        logger.error(f"❌ Erro ao encerrar aplicação: {e}")

# 4. Endpoints da API refatorados para usar Depends

@app.get("/", tags=["Root"])
async def root():
    """Endpoint raiz com informações da API"""
    return {
        "message": "Bem-vindo ao Artell API! 🎨",
        "version": settings.APP_VERSION,
        "docs": "/docs",
    }

@app.get("/health", tags=["Health"])
async def health_check(
    db_service: DatabaseService = Depends(get_database_service) # Injetar dependência
):
    """Endpoint de verificação de saúde da aplicação"""
    return {
        "status": "healthy",
        "service": "Artell API",
        "database": "connected" if db_service.client else "disconnected"
    }


# Os endpoints que estavam duplicados (/analises-recentes, /estatisticas) foram removidos
# pois já estão corretamente definidos e incluídos a partir de 'analyses_router'.

# Executar aplicação se chamado diretamente
if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )