from fastapi import APIRouter, HTTPException, Query
from typing import Optional, List
import logging
from app.services.analysis_service import analysis_service
from app.models.analysis import AnalysisResponse, AnalysisList

logger = logging.getLogger(__name__)
router = APIRouter()

@router.get("/", response_model=AnalysisList)
async def get_analyses(
    page: int = Query(1, ge=1, description="Número da página"),
    limit: int = Query(10, ge=1, le=100, description="Itens por página"),
    artwork_name: Optional[str] = Query(None, description="Filtrar por nome da obra"),
    artist_name: Optional[str] = Query(None, description="Filtrar por nome do artista"),
    style: Optional[str] = Query(None, description="Filtrar por estilo artístico")
):
    """
    Lista todas as análises realizadas com paginação e filtros opcionais.
    
    - **page**: Número da página (começa em 1)
    - **limit**: Itens por página (máximo 100)
    - **artwork_name**: Filtrar por nome da obra
    - **artist_name**: Filtrar por nome do artista
    - **style**: Filtrar por estilo artístico
    """
    try:
        analyses, total = await analysis_service.get_analyses(
            page=page,
            limit=limit,
            artwork_name=artwork_name,
            artist_name=artist_name,
            style=style
        )
        
        return AnalysisList(
            analyses=analyses,
            total=total,
            page=page,
            limit=limit
        )
        
    except Exception as e:
        logger.error(f"Erro ao buscar análises: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{analysis_id}", response_model=AnalysisResponse)
async def get_analysis_by_id(analysis_id: str):
    """
    Obtém uma análise específica pelo ID.
    
    - **analysis_id**: ID único da análise
    """
    try:
        analysis = await analysis_service.get_analysis_by_id(analysis_id)
        
        if not analysis:
            raise HTTPException(
                status_code=404,
                detail="Análise não encontrada"
            )
        
        return analysis
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erro ao buscar análise por ID: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/search/{artwork_name}", response_model=List[AnalysisResponse])
async def search_analyses_by_name(artwork_name: str):
    """
    Pesquisa análises pelo nome da obra de arte.
    
    - **artwork_name**: Nome da obra para pesquisar
    """
    try:
        analyses = await analysis_service.search_analyses_by_name(artwork_name)
        return analyses
        
    except Exception as e:
        logger.error(f"Erro na pesquisa por nome: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/recent/", response_model=List[AnalysisResponse])
async def get_recent_analyses(
    limit: int = Query(5, ge=1, le=20, description="Número de análises recentes")
):
    """
    Obtém as análises mais recentes.
    
    - **limit**: Número de análises recentes (máximo 20)
    """
    try:
        analyses = await analysis_service.get_recent_analyses(limit)
        return analyses
        
    except Exception as e:
        logger.error(f"Erro ao buscar análises recentes: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/stats/summary")
async def get_analysis_stats():
    """
    Obtém estatísticas resumidas das análises.
    """
    try:
        stats = await analysis_service.get_analysis_stats()
        return stats
        
    except Exception as e:
        logger.error(f"Erro ao buscar estatísticas: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/{analysis_id}")
async def delete_analysis(analysis_id: str):
    """
    Remove uma análise específica.
    
    - **analysis_id**: ID único da análise a remover
    """
    try:
        success = await analysis_service.delete_analysis(analysis_id)
        
        if not success:
            raise HTTPException(
                status_code=404,
                detail="Análise não encontrada"
            )
        
        return {"message": "Análise removida com sucesso"}
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erro ao remover análise: {e}")
        raise HTTPException(status_code=500, detail=str(e))
