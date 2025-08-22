# /backend/app/routers/analyses.py

from fastapi import APIRouter, HTTPException, Query, Depends
from typing import Optional, List
import logging
from app.services.analysis_service import get_analysis_service, AnalysisService

# ✨ 1. Alterar a importação para usar o modelo correto
from app.models.artwork_analysis import ArtworkAnalysisResponse

logger = logging.getLogger(__name__)
router = APIRouter()

# ✨ 2. (Opcional, mas recomendado) Criar um modelo para a lista
#    Como o AnalysisList estava no outro ficheiro, vamos definir um aqui
#    ou simplesmente devolver uma Lista. Para simplicidade, vamos devolver List.
@router.get("/", response_model=List[ArtworkAnalysisResponse])
async def get_analyses(
    # ... (o resto da função get_analyses pode ficar como está, mas o response_model muda)
    # NOTE: Para uma implementação completa, você criaria um ArtworkAnalysisList
    # similar ao que tinha, mas usando ArtworkAnalysisResponse.
    # Por agora, vamos focar em corrigir o erro principal.
    page: int = Query(1, ge=1, description="Número da página"),
    limit: int = Query(10, ge=1, le=100, description="Itens por página"),
    artwork_name: Optional[str] = Query(None, description="Filtrar por nome da obra"),
    artist_name: Optional[str] = Query(None, description="Filtrar por nome do artista"),
    style: Optional[str] = Query(None, description="Filtrar por estilo artístico"),
    analysis_service: AnalysisService = Depends(get_analysis_service)
):
    # Esta função pode precisar de mais ajustes para paginar corretamente,
    # mas a correção principal é o response_model.
    analyses, total = await analysis_service.get_analyses(
        page=page, limit=limit, artwork_name=artwork_name, artist_name=artist_name, style=style
    )
    return analyses # Devolve a lista diretamente

@router.get("/{analysis_id}", response_model=ArtworkAnalysisResponse) # ✨ 3. Mudar o response_model aqui
async def get_analysis_by_id(
    analysis_id: str,
    analysis_service: AnalysisService = Depends(get_analysis_service)
):
    try:
        # O serviço já devolve o tipo correto (ArtworkAnalysisResponse),
        # por isso não precisamos de mudar a lógica aqui.
        analysis = await analysis_service.get_analysis_by_id(analysis_id)
        if not analysis:
            raise HTTPException(status_code=404, detail="Análise não encontrada")
        return analysis
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erro ao buscar análise por ID: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# ... (aplique a mesma alteração do response_model para os outros endpoints se necessário) ...

@router.get("/recent/", response_model=List[ArtworkAnalysisResponse]) # ✨ 4. Mudar também aqui
async def get_recent_analyses(
    limit: int = Query(5, ge=1, le=20, description="Número de análises recentes"),
    analysis_service: AnalysisService = Depends(get_analysis_service)
):
    try:
        analyses = await analysis_service.get_recent_analyses(limit)
        return analyses
    except Exception as e:
        logger.error(f"Erro ao buscar análises recentes: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# ... resto do ficheiro ...

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