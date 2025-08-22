# /backend/app/services/analysis_service.py
from functools import lru_cache
from typing import List, Optional, Tuple
import logging
from fastapi import Depends
from app.models.analysis import AnalysisCreate, AnalysisResponse
from app.services.database_service import database_service # Removido 'get_collection' e importado o 'database_service'
from app.services.database_service import get_database_service, DatabaseService


logger = logging.getLogger(__name__)

class AnalysisService:
    def __init__(self, db_service: DatabaseService = Depends(get_database_service)):
        self.db_service = db_service
    """
    Este serviço age como uma camada de lógica de negócio,
    delegando as operações de base de dados para o 'database_service'.
    """
    async def create_analysis(self, analysis: AnalysisCreate) -> AnalysisResponse:
        # Usar a instância injetada
        return await self.db_service.save_analysis(analysis.dict())
    
    async def get_analysis_by_id(self, analysis_id: str) -> Optional[AnalysisResponse]:
        # Usar a instância injetada
        return await self.db_service.get_analysis_by_id(analysis_id)
    # ... (adapte as outras funções para usar self.db_service)

    async def create_analysis(self, analysis: AnalysisCreate) -> AnalysisResponse:
        """Cria uma nova análise na base de dados"""
        try:
            # Converte o modelo Pydantic para um dicionário
            analysis_dict = analysis.dict()
            # Delega a operação de salvar para o database_service
            saved_analysis = await database_service.save_analysis(analysis_dict)
            return saved_analysis
        except Exception as e:
            logger.error(f"Erro ao criar análise no service: {e}")
            raise e
    
    async def get_analysis_by_id(self, analysis_id: str) -> Optional[AnalysisResponse]:
        """Obtém uma análise pelo ID"""
        try:
            # Delega a busca por ID para o database_service
            return await database_service.get_analysis_by_id(analysis_id)
        except Exception as e:
            logger.error(f"Erro ao buscar análise por ID no service: {e}")
            raise e
    
    async def get_analysis_by_image_hash(self, image_hash: str) -> Optional[AnalysisResponse]:
        """Obtém uma análise pelo hash da imagem (para cache)"""
        try:
            # Delega a busca por hash para o database_service
            return await database_service.get_analysis_by_image_hash(image_hash)
        except Exception as e:
            logger.error(f"Erro ao buscar análise por hash no service: {e}")
            raise e
    
    async def get_analysis_by_name(self, artwork_name: str) -> Optional[AnalysisResponse]:
        """Obtém uma análise pelo nome da obra (para cache)"""
        try:
            # Delega a busca por nome para o database_service
            return await database_service.get_analysis_by_name(artwork_name)
        except Exception as e:
            logger.error(f"Erro ao buscar análise por nome no service: {e}")
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
            # Delega a listagem para o database_service
            return await database_service.get_analyses(
                page=page,
                limit=limit,
                artwork_name=artwork_name,
                artist_name=artist_name,
                style=style
            )
        except Exception as e:
            logger.error(f"Erro ao buscar análises no service: {e}")
            raise e
    
    async def search_analyses_by_name(self, artwork_name: str) -> List[AnalysisResponse]:
        """Pesquisa análises pelo nome da obra"""
        try:
            # Delega a pesquisa para o database_service
            return await database_service.search_analyses_by_name(artwork_name)
        except Exception as e:
            logger.error(f"Erro na pesquisa por nome no service: {e}")
            raise e
    
    async def get_recent_analyses(self, limit: int = 5) -> List[AnalysisResponse]:
        """Obtém as análises mais recentes"""
        try:
            # Delega a busca de recentes para o database_service
            return await database_service.get_recent_analyses(limit)
        except Exception as e:
            logger.error(f"Erro ao buscar análises recentes no service: {e}")
            raise e
    
    async def get_analysis_stats(self) -> dict:
        """Obtém estatísticas das análises"""
        try:
            # Delega a busca de estatísticas para o database_service
            return await database_service.get_analysis_stats()
        except Exception as e:
            logger.error(f"Erro ao buscar estatísticas no service: {e}")
            raise e
    
    async def delete_analysis(self, analysis_id: str) -> bool:
        """Remove uma análise"""
        try:
            # Delega a remoção para o database_service
            return await database_service.delete_analysis(analysis_id)
        except Exception as e:
            logger.error(f"Erro ao remover análise no service: {e}")
            raise e
        
@lru_cache()
def get_analysis_service() -> AnalysisService:
    """
    Cria e retorna uma instância singleton do AnalysisService.
    O lru_cache garante que a mesma instância seja reutilizada em todo o pedido.
    """
    return AnalysisService()