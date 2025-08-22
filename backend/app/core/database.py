from motor.motor_asyncio import AsyncIOMotorClient
from app.core.config import settings
import logging

logger = logging.getLogger(__name__)

class Database:
    client: AsyncIOMotorClient = None
    database = None

db = Database()

async def get_database() -> AsyncIOMotorClient:
    return db.client

async def get_collection(collection_name: str):
    database = await get_database()
    return database.artell[collection_name]

async def init_db():
    try:
        db.client = AsyncIOMotorClient(settings.MONGODB_URI)
        db.database = db.client.artell
        
        # Testa a conexão
        await db.client.admin.command('ping')
        logger.info("✅ Conectado ao MongoDB com sucesso!")
        
        # Cria índices para otimização
        await create_indexes()
        
    except Exception as e:
        logger.error(f"❌ Erro ao conectar ao MongoDB: {e}")
        raise e

async def create_indexes():
    """Cria índices para otimizar as consultas"""
    try:
        # Índice para análises por hash da imagem
        await db.database.analyses.create_index("image_hash")
        
        # Índice para análises por nome da obra
        await db.database.analyses.create_index("artwork_name")
        
        # Índice para análises por data
        await db.database.analyses.create_index("created_at")
        
        logger.info("✅ Índices criados com sucesso!")
        
    except Exception as e:
        logger.error(f"❌ Erro ao criar índices: {e}")

async def close_db():
    if db.client:
        db.client.close()
        logger.info("✅ Conexão com MongoDB fechada!")
