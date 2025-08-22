import logging
from typing import Optional, List
from motor.motor_asyncio import AsyncIOMotorClient
from app.core.config import settings
from app.models.artwork_analysis import ArtworkAnalysisDB, ArtworkAnalysisResponse

logger = logging.getLogger(__name__)

class DatabaseService:
    """Serviço para gerenciar operações na base de dados MongoDB"""
    
    def __init__(self):
        self.client: Optional[AsyncIOMotorClient] = None
        self.db = None
        self.collection_name = "artwork_analyses"
    
    async def connect(self):
        """Conecta à base de dados MongoDB"""
        try:
            # Usar a URI completa com autenticação
            self.client = AsyncIOMotorClient(settings.MONGODB_URI)
            
            # Conectar ao banco artell
            self.db = self.client.artell
            
            # Testar conexão
            await self.client.admin.command('ping')
            logger.info("✅ Conectado ao MongoDB com sucesso!")
            
            # Criar índices para otimização
            await self._create_indexes()
            
        except Exception as e:
            logger.error(f"❌ Erro ao conectar ao MongoDB: {e}")
            raise e
    
    async def disconnect(self):
        """Desconecta da base de dados"""
        if self.client:
            self.client.close()
            logger.info("✅ Conexão com MongoDB fechada!")
    
    async def _create_indexes(self):
        """Cria índices para otimizar consultas"""
        try:
            collection = self.db[self.collection_name]
            
            # Criar índices
            await collection.create_index("artwork_name")
            await collection.create_index("created_at")
            await collection.create_index("artist")
            
            logger.info("✅ Índices criados com sucesso!")
            
        except Exception as e:
            logger.error(f"❌ Erro ao criar índices: {e}")
            # Não falhar a aplicação se os índices não puderem ser criados
            logger.warning("⚠️ Aplicação continuará sem índices otimizados")
    
    async def get_analysis_by_name(self, artwork_name: str) -> Optional[ArtworkAnalysisResponse]:
        """
        Busca uma análise existente na base de dados
        
        Args:
            artwork_name: Nome da obra de arte
            
        Returns:
            Análise se encontrada, None caso contrário
        """
        try:
            collection = self.db[self.collection_name]
            
            # Busca case-insensitive por nome da obra
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
    
    async def save_analysis(self, analysis_data: dict) -> ArtworkAnalysisResponse:
        """
        Salva uma nova análise na base de dados
        
        Args:
            analysis_data: Dados da análise a ser salva
            
        Returns:
            Análise salva com ID e timestamps
        """
        try:
            collection = self.db[self.collection_name]
            
            # Criar documento para salvar
            analysis_doc = ArtworkAnalysisDB(**analysis_data)
            analysis_dict = analysis_doc.dict()
            
            # Inserir na base de dados
            result = await collection.insert_one(analysis_dict)
            
            # Atualizar ID e retornar
            analysis_dict["_id"] = str(result.inserted_id)
            
            logger.info(f"Análise salva na base de dados: {analysis_data['artwork_name']}")
            
            return self._convert_to_response(analysis_dict, cached=False)
            
        except Exception as e:
            logger.error(f"Erro ao salvar análise: {e}")
            raise Exception(f"Erro ao salvar análise: {str(e)}")
    
    async def get_recent_analyses(self, limit: int = 10) -> List[ArtworkAnalysisResponse]:
        """
        Obtém as análises mais recentes
        
        Args:
            limit: Número máximo de análises a retornar
            
        Returns:
            Lista de análises recentes
        """
        try:
            collection = self.db[self.collection_name]
            
            cursor = collection.find().sort("created_at", -1).limit(limit)
            
            analyses = []
            async for doc in cursor:
                analyses.append(self._convert_to_response(doc, cached=True))
            
            return analyses
            
        except Exception as e:
            logger.error(f"Erro ao buscar análises recentes: {e}")
            return []
    
    async def get_analysis_stats(self) -> dict:
        """
        Obtém estatísticas das análises
        
        Returns:
            Dicionário com estatísticas
        """
        try:
            collection = self.db[self.collection_name]
            
            # Total de análises
            total = await collection.count_documents({})
            
            # Análises por artista (top 5)
            pipeline = [
                {"$group": {"_id": "$artist", "count": {"$sum": 1}}},
                {"$sort": {"count": -1}},
                {"$limit": 5}
            ]
            
            top_artists = []
            async for doc in collection.aggregate(pipeline):
                if doc["_id"]:  # Ignorar artistas nulos
                    top_artists.append({
                        "artist": doc["_id"],
                        "count": doc["count"]
                    })
            
            return {
                "total_analyses": total,
                "top_artists": top_artists
            }
            
        except Exception as e:
            logger.error(f"Erro ao buscar estatísticas: {e}")
            return {"total_analyses": 0, "top_artists": []}
    
    def _convert_to_response(self, doc: dict, cached: bool) -> ArtworkAnalysisResponse:
        """
        Converte documento da base de dados para resposta da API
        
        Args:
            doc: Documento do MongoDB
            cached: Indica se veio do cache
            
        Returns:
            Objeto ArtworkAnalysisResponse
        """
        return ArtworkAnalysisResponse(
            artwork=doc["artwork_name"],
            analysis=doc["analysis"],
            artist=doc.get("artist"),
            year=doc.get("year"),
            style=doc.get("style"),
            emotions=doc.get("emotions", []),
            processing_time=doc["processing_time"],
            cached=cached
        )

# Instância global do serviço
database_service = DatabaseService()
