# backend/app/services/database_service.py

import logging
from typing import Optional, List, Tuple
from motor.motor_asyncio import AsyncIOMotorClient
from bson import ObjectId
from app.core.config import settings
from app.models.artwork_analysis import ArtworkAnalysisDB, ArtworkAnalysisResponse, ArtworkAnalysisCreate
from functools import lru_cache

logger = logging.getLogger(__name__)

class DatabaseService:
    """Serviço para gerenciar operações na base de dados MongoDB"""
        
    def __init__(self):
        self.client: Optional[AsyncIOMotorClient] = None
        self.db = None
        self.collection_name = "artwork_analyses"
    
    async def connect(self):
        try:
            self.client = AsyncIOMotorClient(settings.MONGODB_URI)
            self.db = self.client.artell
            await self.client.admin.command('ping')
            logger.info("✅ Conectado ao MongoDB com sucesso!")
            await self._create_indexes()
        except Exception as e:
            logger.error(f"❌ Erro ao conectar ao MongoDB: {e}")
            raise e
    
    async def disconnect(self):
        if self.client:
            self.client.close()
            logger.info("✅ Conexão com MongoDB fechada!")
    
    async def _create_indexes(self):
        try:
            collection = self.db[self.collection_name]
            await collection.create_index("artwork_name")
            await collection.create_index("image_hash")
            await collection.create_index("created_at")
            await collection.create_index("artist")
            logger.info("✅ Índices criados com sucesso!")
        except Exception as e:
            logger.error(f"❌ Erro ao criar índices: {e}")
            logger.warning("⚠️ Aplicação continuará sem índices otimizados")

    async def get_analysis_by_image_hash(self, image_hash: str) -> Optional[ArtworkAnalysisResponse]:
        try:
            collection = self.db[self.collection_name]
            result = await collection.find_one({"image_hash": image_hash})
            if result:
                logger.info(f"Análise encontrada em cache pelo hash da imagem: {image_hash[:10]}...")
                return self._convert_to_response(result, cached=True)
            return None
        except Exception as e:
            logger.error(f"Erro ao buscar análise por hash de imagem: {e}")
            return None

    async def get_analysis_by_name(self, artwork_name: str) -> Optional[ArtworkAnalysisResponse]:
        try:
            collection = self.db[self.collection_name]
            result = await collection.find_one({
                "artwork_name": {"$regex": f"^{artwork_name}$", "$options": "i"}
            })
            if result:
                logger.info(f"Análise encontrada em cache para: {artwork_name}")
                return self._convert_to_response(result, cached=True)
            return None
        except Exception as e:
            logger.error(f"Erro ao buscar análise por nome: {e}")
            return None
    
    async def save_analysis(self, analysis_data: dict, image_hash: Optional[str] = None) -> ArtworkAnalysisResponse:
        try:
            collection = self.db[self.collection_name]
            if image_hash:
                analysis_data['image_hash'] = image_hash

            analysis_to_create = ArtworkAnalysisCreate(**analysis_data)
            analysis_doc = ArtworkAnalysisDB(**analysis_to_create.dict())
            analysis_dict = analysis_doc.dict()
            
            result = await collection.insert_one(analysis_dict)
            analysis_dict["_id"] = result.inserted_id
            
            logger.info(f"Análise salva na base de dados: {analysis_data['artwork_name']}")
            return self._convert_to_response(analysis_dict, cached=False)
        except Exception as e:
            logger.error(f"Erro ao salvar análise: {e}")
            raise Exception(f"Erro ao salvar análise: {str(e)}")
    
    async def get_recent_analyses(self, limit: int = 10) -> List[ArtworkAnalysisResponse]:
        try:
            collection = self.db[self.collection_name]
            cursor = collection.find().sort("created_at", -1).limit(limit)
            analyses = [self._convert_to_response(doc, cached=True) async for doc in cursor]
            return analyses
        except Exception as e:
            logger.error(f"Erro ao buscar análises recentes: {e}")
            return []

    async def get_analysis_by_id(self, analysis_id: str) -> Optional[ArtworkAnalysisResponse]:
        try:
            collection = self.db[self.collection_name]
            if not ObjectId.is_valid(analysis_id):
                return None
            result = await collection.find_one({"_id": ObjectId(analysis_id)})
            if result:
                return self._convert_to_response(result, cached=True)
            return None
        except Exception as e:
            logger.error(f"Erro ao buscar análise por ID: {e}")
            return None

    async def get_analyses(
        self, 
        page: int = 1, 
        limit: int = 10,
        artwork_name: Optional[str] = None,
        artist_name: Optional[str] = None,
        style: Optional[str] = None
    ) -> Tuple[List[ArtworkAnalysisResponse], int]:
        try:
            collection = self.db[self.collection_name]
            query = {}
            if artwork_name:
                query["artwork_name"] = {"$regex": artwork_name, "$options": "i"}
            if artist_name:
                query["artist"] = {"$regex": artist_name, "$options": "i"}
            if style:
                query["style"] = {"$regex": style, "$options": "i"}

            total = await collection.count_documents(query)
            skip_count = (page - 1) * limit
            cursor = collection.find(query).skip(skip_count).limit(limit)
            analyses = [self._convert_to_response(doc, cached=True) async for doc in cursor]
            
            return analyses, total
        except Exception as e:
            logger.error(f"Erro ao buscar análises paginadas: {e}")
            return [], 0

    async def get_analysis_stats(self) -> dict:
        try:
            collection = self.db[self.collection_name]
            total = await collection.count_documents({})
            return {"total_analyses": total}
        except Exception as e:
            logger.error(f"Erro ao buscar estatísticas: {e}")
            return {"total_analyses": 0}
            
    def _convert_to_response(self, doc: dict, cached: bool) -> ArtworkAnalysisResponse:
        """Converte documento da base de dados para resposta da API."""
        return ArtworkAnalysisResponse(
            id=str(doc['_id']),
            artwork_name=doc["artwork_name"],
            analysis=doc["analysis"],
            artist=doc.get("artist"),
            year=doc.get("year"),
            style=doc.get("style"),
            emotions=doc.get("emotions", []),
            image_url=doc.get("image_url"), # <-- ✨ CORREÇÃO AQUI
            processing_time=doc.get("processing_time", 0.0),
            cached=cached
        )

@lru_cache()
def get_database_service() -> DatabaseService:
    return DatabaseService()