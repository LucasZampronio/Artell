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

# Eventos de startup e shutdown
@app.on_event("startup")
async def startup_event():
    """Evento executado na inicialização da aplicação"""
    try:
        logger.info("🚀 Iniciando aplicação Artell com Groq...")
        
        # Conectar à base de dados
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
        
        # Desconectar da base de dados
        await database_service.disconnect()
        
        logger.info("✅ Aplicação encerrada com sucesso!")
        
    except Exception as e:
        logger.error(f"❌ Erro ao encerrar aplicação: {e}")

# Endpoints da API

@app.get("/")
async def root():
    """Endpoint raiz com informações da API"""
    return {
        "message": "Bem-vindo ao Artell API! 🎨",
        "version": settings.APP_VERSION,
        "description": "API para análise de obras de arte usando inteligência artificial (Groq)",
        "ai_provider": "Groq (Llama 4 Scout)",
        "docs": "/docs",
        "endpoints": {
            "analyze_by_name": "POST /analise-por-nome",
            "recent_analyses": "GET /analises-recentes",
            "stats": "GET /estatisticas"
        }
    }

@app.get("/health")
async def health_check():
    """Endpoint de verificação de saúde da aplicação"""
    return {
        "status": "healthy",
        "service": "Artell API",
        "version": settings.APP_VERSION,
        "ai_provider": "Groq",
        "database": "connected" if database_service.client else "disconnected"
    }

@app.post("/analise-por-nome", response_model=ArtworkAnalysisResponse)
async def analyze_artwork_by_name(request: ArtworkAnalysisRequest):
    """
    Analisa uma obra de arte pelo nome usando IA (Groq)
    
    Este endpoint implementa um sistema de cache inteligente:
    1. Primeiro verifica se a análise já existe no MongoDB
    2. Se existir, retorna a análise em cache
    3. Se não existir, chama a API da Groq
    4. Salva a nova análise no MongoDB para futuras consultas
    """
    try:
        artwork_name = request.artwork_name.strip()
        
        if not artwork_name:
            raise HTTPException(
                status_code=400,
                detail="Nome da obra de arte é obrigatório"
            )
        
        logger.info(f"🔍 Recebida requisição para analisar: {artwork_name}")
        
        # 1. Verificar se já existe análise em cache
        cached_analysis = await database_service.get_analysis_by_name(artwork_name)
        
        if cached_analysis:
            logger.info(f"✅ Análise encontrada em cache para: {artwork_name}")
            return cached_analysis
        
        # 2. Se não existir, gerar nova análise com Groq
        logger.info(f"🤖 Gerando nova análise com Groq para: {artwork_name}")
        
        analysis_data = await groq_service.analyze_artwork(artwork_name)
        
        # 3. Salvar análise na base de dados
        saved_analysis = await database_service.save_analysis(analysis_data)
        
        logger.info(f"💾 Análise salva na base de dados: {artwork_name}")
        
        return saved_analysis
        
    except HTTPException:
        # Re-raise HTTP exceptions
        raise
    except Exception as e:
        logger.error(f"❌ Erro na análise da obra {request.artwork_name}: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Erro interno do servidor: {str(e)}"
        )

@app.get("/analises-recentes")
async def get_recent_analyses(limit: int = 10):
    """
    Obtém as análises mais recentes
    
    Args:
        limit: Número máximo de análises a retornar (padrão: 10)
    """
    try:
        if limit < 1 or limit > 50:
            raise HTTPException(
                status_code=400,
                detail="Limit deve estar entre 1 e 50"
            )
        
        analyses = await database_service.get_recent_analyses(limit)
        
        return {
            "analyses": analyses,
            "total": len(analyses),
            "limit": limit
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ Erro ao buscar análises recentes: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Erro interno do servidor: {str(e)}"
        )

@app.get("/estatisticas")
async def get_statistics():
    """Obtém estatísticas das análises realizadas"""
    try:
        stats = await database_service.get_analysis_stats()
        
        return {
            "message": "Estatísticas das análises",
            "data": stats
        }
        
    except Exception as e:
        logger.error(f"❌ Erro ao buscar estatísticas: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Erro interno do servidor: {str(e)}"
        )

# Executar aplicação se chamado diretamente
if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )
