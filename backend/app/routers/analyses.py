# /backend/app/routers/analyses.py

from fastapi import APIRouter, HTTPException, Query, Depends # ✨ 1. Importar Depends
from typing import Optional, List
import logging
# ✨ 2. Importar a função 'getter' e a classe do serviço
from app.services.analysis_service import get_analysis_service, AnalysisService 
from app.models.analysis import AnalysisResponse, AnalysisList

logger = logging.getLogger(__name__)
router = APIRouter()

@router.get("/", response_model=AnalysisList)
async def get_analyses(
    page: int = Query(1, ge=1, description="Número da página"),
    limit: int = Query(10, ge=1, le=100, description="Itens por página"),
    artwork_name: Optional[str] = Query(None, description="Filtrar por nome da obra"),
    artist_name: Optional[str] = Query(None, description="Filtrar por nome do artista"),
    style: Optional[str] = Query(None, description="Filtrar por estilo artístico"),
    # ✨ 3. Injetar a dependência
    analysis_service: AnalysisService = Depends(get_analysis_service)
):
    try:
        analyses, total = await analysis_service.get_analyses(
            page=page, limit=limit, artwork_name=artwork_name, artist_name=artist_name, style=style
        )
        return AnalysisList(analyses=analyses, total=total, page=page, limit=limit)
    except Exception as e:
        logger.error(f"Erro ao buscar análises: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{analysis_id}", response_model=AnalysisResponse)
async def get_analysis_by_id(
    analysis_id: str, 
    analysis_service: AnalysisService = Depends(get_analysis_service) # Injetar
):
    try:
        analysis = await analysis_service.get_analysis_by_id(analysis_id)
        if not analysis:
            raise HTTPException(status_code=404, detail="Análise não encontrada")
        return analysis
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erro ao buscar análise por ID: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/search/{artwork_name}", response_model=List[AnalysisResponse])
async def search_analyses_by_name(
    artwork_name: str, 
    analysis_service: AnalysisService = Depends(get_analysis_service) # Injetar
):
    try:
        analyses = await analysis_service.search_analyses_by_name(artwork_name)
        return analyses
    except Exception as e:
        logger.error(f"Erro na pesquisa por nome: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/recent/", response_model=List[AnalysisResponse])
async def get_recent_analyses(
    limit: int = Query(5, ge=1, le=20, description="Número de análises recentes"),
    analysis_service: AnalysisService = Depends(get_analysis_service) # Injetar
):
    try:
        analyses = await analysis_service.get_recent_analyses(limit)
        return analyses
    except Exception as e:
        logger.error(f"Erro ao buscar análises recentes: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/stats/summary")
async def get_analysis_stats(
    analysis_service: AnalysisService = Depends(get_analysis_service) # Injetar
):
    try:
        stats = await analysis_service.get_analysis_stats()
        return stats
    except Exception as e:
        logger.error(f"Erro ao buscar estatísticas: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/{analysis_id}")
async def delete_analysis(
    analysis_id: str,
    analysis_service: AnalysisService = Depends(get_analysis_service) # Injetar
):
    try:
        success = await analysis_service.delete_analysis(analysis_id)
        if not success:
            raise HTTPException(status_code=404, detail="Análise não encontrada")
        return {"message": "Análise removida com sucesso"}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erro ao remover análise: {e}")
        raise HTTPException(status_code=500, detail=str(e))