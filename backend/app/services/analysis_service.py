from typing import List, Optional, Tuple
from bson import ObjectId
from datetime import datetime
import logging
from app.core.database import get_collection
from app.models.analysis import AnalysisCreate, AnalysisResponse, AnalysisType

logger = logging.getLogger(__name__)

class AnalysisService:
    def __init__(self):
        self.collection_name = "analyses"
    
    async def create_analysis(self, analysis: AnalysisCreate) -> AnalysisResponse:
        """Cria uma nova análise na base de dados"""
        try:
            collection = await get_collection(self.collection_name)
            
            # Converte para dict e adiciona timestamp
            analysis_dict = analysis.dict()
            analysis_dict["created_at"] = datetime.utcnow()
            analysis_dict["_id"] = ObjectId()
            
            # Insere na base de dados
            result = await collection.insert_one(analysis_dict)
            
            # Retorna a análise criada
            return await self.get_analysis_by_id(str(result.inserted_id))
            
        except Exception as e:
            logger.error(f"Erro ao criar análise: {e}")
            raise e
    
    async def get_analysis_by_id(self, analysis_id: str) -> Optional[AnalysisResponse]:
        """Obtém uma análise pelo ID"""
        try:
            collection = await get_collection(self.collection_name)
            
            # Busca por ObjectId
            if not ObjectId.is_valid(analysis_id):
                return None
            
            result = await collection.find_one({"_id": ObjectId(analysis_id)})
            
            if result:
                return self._convert_to_response(result)
            
            return None
            
        except Exception as e:
            logger.error(f"Erro ao buscar análise por ID: {e}")
            raise e
    
    async def get_analysis_by_image_hash(self, image_hash: str) -> Optional[AnalysisResponse]:
        """Obtém uma análise pelo hash da imagem (para cache)"""
        try:
            collection = await get_collection(self.collection_name)
            
            result = await collection.find_one({"image_hash": image_hash})
            
            if result:
                return self._convert_to_response(result)
            
            return None
            
        except Exception as e:
            logger.error(f"Erro ao buscar análise por hash: {e}")
            raise e
    
    async def get_analysis_by_name(self, artwork_name: str) -> Optional[AnalysisResponse]:
        """Obtém uma análise pelo nome da obra (para cache)"""
        try:
            collection = await get_collection(self.collection_name)
            
            # Busca case-insensitive
            result = await collection.find_one({
                "artwork_name": {"$regex": f"^{artwork_name}$", "$options": "i"}
            })
            
            if result:
                return self._convert_to_response(result)
            
            return None
            
        except Exception as e:
            logger.error(f"Erro ao buscar análise por nome: {e}")
            raise e
    
    async def get_analyses(
        self, 
        page: int = 1, 
        limit: int = 10,
        artwork_name: Optional[str] = None,
        artist_name: Optional[str] = None,
        style: Optional[str] = None
    ) -> Tuple[List[AnalysisResponse], int]:
        """Lista análises com paginação e filtros"""
        try:
            collection = await get_collection(self.collection_name)
            
            # Constrói filtros
            filters = {}
            if artwork_name:
                filters["artwork_name"] = {"$regex": artwork_name, "$options": "i"}
            if artist_name:
                filters["artist_name"] = {"$regex": artist_name, "$options": "i"}
            if style:
                filters["style"] = style
            
            # Conta total de documentos
            total = await collection.count_documents(filters)
            
            # Calcula skip para paginação
            skip = (page - 1) * limit
            
            # Busca documentos com paginação
            cursor = collection.find(filters).sort("created_at", -1).skip(skip).limit(limit)
            
            analyses = []
            async for doc in cursor:
                analyses.append(self._convert_to_response(doc))
            
            return analyses, total
            
        except Exception as e:
            logger.error(f"Erro ao buscar análises: {e}")
            raise e
    
    async def search_analyses_by_name(self, artwork_name: str) -> List[AnalysisResponse]:
        """Pesquisa análises pelo nome da obra"""
        try:
            collection = await get_collection(self.collection_name)
            
            # Busca case-insensitive e parcial
            cursor = collection.find({
                "artwork_name": {"$regex": artwork_name, "$options": "i"}
            }).sort("created_at", -1).limit(20)
            
            analyses = []
            async for doc in cursor:
                analyses.append(self._convert_to_response(doc))
            
            return analyses
            
        except Exception as e:
            logger.error(f"Erro na pesquisa por nome: {e}")
            raise e
    
    async def get_recent_analyses(self, limit: int = 5) -> List[AnalysisResponse]:
        """Obtém as análises mais recentes"""
        try:
            collection = await get_collection(self.collection_name)
            
            cursor = collection.find().sort("created_at", -1).limit(limit)
            
            analyses = []
            async for doc in cursor:
                analyses.append(self._convert_to_response(doc))
            
            return analyses
            
        except Exception as e:
            logger.error(f"Erro ao buscar análises recentes: {e}")
            raise e
    
    async def get_analysis_stats(self) -> dict:
        """Obtém estatísticas das análises"""
        try:
            collection = await get_collection(self.collection_name)
            
            # Total de análises
            total_analyses = await collection.count_documents({})
            
            # Análises por tipo
            image_analyses = await collection.count_documents({"analysis_type": AnalysisType.IMAGE})
            text_analyses = await collection.count_documents({"analysis_type": AnalysisType.TEXT})
            
            # Análises por estilo
            pipeline = [
                {"$group": {"_id": "$style", "count": {"$sum": 1}}},
                {"$sort": {"count": -1}},
                {"$limit": 5}
            ]
            
            style_stats = []
            async for doc in collection.aggregate(pipeline):
                style_stats.append({
                    "style": doc["_id"] or "unknown",
                    "count": doc["count"]
                })
            
            return {
                "total_analyses": total_analyses,
                "by_type": {
                    "image": image_analyses,
                    "text": text_analyses
                },
                "top_styles": style_stats
            }
            
        except Exception as e:
            logger.error(f"Erro ao buscar estatísticas: {e}")
            raise e
    
    async def delete_analysis(self, analysis_id: str) -> bool:
        """Remove uma análise"""
        try:
            collection = await get_collection(self.collection_name)
            
            if not ObjectId.is_valid(analysis_id):
                return False
            
            result = await collection.delete_one({"_id": ObjectId(analysis_id)})
            
            return result.deleted_count > 0
            
        except Exception as e:
            logger.error(f"Erro ao remover análise: {e}")
            raise e
    
    def _convert_to_response(self, doc: dict) -> AnalysisResponse:
        """Converte documento da base de dados para AnalysisResponse"""
        return AnalysisResponse(
            id=str(doc["_id"]),
            artwork_name=doc["artwork_name"],
            artist_name=doc.get("artist_name"),
            year_created=doc.get("year_created"),
            style=doc.get("style"),
            meaning=doc["meaning"],
            artist_intention=doc["artist_intention"],
            emotions=doc["emotions"],
            emotional_description=doc["emotional_description"],
            analysis_type=doc["analysis_type"],
            image_hash=doc.get("image_hash"),
            created_at=doc["created_at"],
            processing_time=doc["processing_time"]
        )

# Instância global do serviço
analysis_service = AnalysisService()
