# /backend/main.py

from fastapi import FastAPI, HTTPException, Depends # 1. Adicionar Depends
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from dotenv import load_dotenv
import logging

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

@app.post("/analise-por-nome", response_model=ArtworkAnalysisResponse, tags=["Analysis"])
async def analyze_artwork_by_name(
    request: ArtworkAnalysisRequest,
    db_service: DatabaseService = Depends(get_database_service), # Injetar DatabaseService
    groq_service: GroqService = Depends(get_groq_service) # Injetar GroqService
):
    """
    Analisa uma obra de arte pelo nome usando IA (Groq)
    """
    try:
        artwork_name = request.artwork_name.strip()
        if not artwork_name:
            raise HTTPException(status_code=400, detail="Nome da obra de arte é obrigatório")
        
        logger.info(f"🔍 Recebida requisição para analisar: {artwork_name}")
        
        # Usar as instâncias injetadas (db_service, groq_service)
        cached_analysis = await db_service.get_analysis_by_name(artwork_name)
        if cached_analysis:
            logger.info(f"✅ Análise encontrada em cache para: {artwork_name}")
            return cached_analysis
        
        logger.info(f"🤖 Gerando nova análise com Groq para: {artwork_name}")
        analysis_data = await groq_service.analyze_artwork(artwork_name)
        
        saved_analysis = await db_service.save_analysis(analysis_data)
        logger.info(f"💾 Análise salva na base de dados: {artwork_name}")
        
        return saved_analysis
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ Erro na análise da obra {request.artwork_name}: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Erro interno do servidor: {str(e)}")

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