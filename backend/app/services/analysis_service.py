# /backend/app/services/analysis_service.py

from fastapi import Depends
from functools import lru_cache
from typing import List, Optional, Tuple
import logging

from app.models.analysis import AnalysisCreate, AnalysisResponse
from app.services.database_service import get_database_service, DatabaseService

logger = logging.getLogger(__name__)

class AnalysisService:
    def __init__(self, db_service: DatabaseService = Depends(get_database_service)):
        self.db_service = db_service
    
    async def create_analysis(self, analysis: AnalysisCreate) -> AnalysisResponse:
        try:
            analysis_dict = analysis.dict()
            return await self.db_service.save_analysis(analysis_dict)
        except Exception as e:
            logger.error(f"Erro ao criar análise no service: {e}")
            raise e
    
    async def get_analysis_by_id(self, analysis_id: str) -> Optional[AnalysisResponse]:
        try:
            return await self.db_service.get_analysis_by_id(analysis_id)
        except Exception as e:
            logger.error(f"Erro ao buscar análise por ID no service: {e}")
            raise e
    
    async def get_analysis_by_image_hash(self, image_hash: str) -> Optional[AnalysisResponse]:
        try:
            return await self.db_service.get_analysis_by_image_hash(image_hash)
        except Exception as e:
            logger.error(f"Erro ao buscar análise por hash no service: {e}")
            raise e
    
    async def get_analysis_by_name(self, artwork_name: str) -> Optional[AnalysisResponse]:
        try:
            return await self.db_service.get_analysis_by_name(artwork_name)
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
        try:
            return await self.db_service.get_analyses(
                page=page, limit=limit, artwork_name=artwork_name, artist_name=artist_name, style=style
            )
        except Exception as e:
            logger.error(f"Erro ao buscar análises no service: {e}")
            raise e
    
    async def search_analyses_by_name(self, artwork_name: str) -> List[AnalysisResponse]:
        try:
            return await self.db_service.search_analyses_by_name(artwork_name)
        except Exception as e:
            logger.error(f"Erro na pesquisa por nome no service: {e}")
            raise e
    
    async def get_recent_analyses(self, limit: int = 5) -> List[AnalysisResponse]:
        try:
            return await self.db_service.get_recent_analyses(limit)
        except Exception as e:
            logger.error(f"Erro ao buscar análises recentes no service: {e}")
            raise e
    
    async def get_analysis_stats(self) -> dict:
        try:
            return await self.db_service.get_analysis_stats()
        except Exception as e:
            logger.error(f"Erro ao buscar estatísticas no service: {e}")
            raise e
    
    async def delete_analysis(self, analysis_id: str) -> bool:
        try:
            return await self.db_service.delete_analysis(analysis_id)
        except Exception as e:
            logger.error(f"Erro ao remover análise no service: {e}")
            raise e

@lru_cache()
def get_analysis_service() -> AnalysisService:
    """
    Cria e retorna uma instância singleton do AnalysisService.
    """
    # ✨ CORREÇÃO: Removidos os parênteses extra a seguir a get_database_service()
    return AnalysisService(db_service=get_database_service())