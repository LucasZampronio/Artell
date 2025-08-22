# backend/app/models/artwork_analysis.py

from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime

class ArtworkAnalysisRequest(BaseModel):
    """Modelo para requisição de análise de obra de arte por nome."""
    artwork_name: str = Field(
        ..., 
        description="Nome da obra de arte a ser analisada",
        min_length=1,
        max_length=200,
        example="A Noite Estrelada"
    )

# ✨✨ INÍCIO DO CÓDIGO ADICIONADO ✨✨
class ArtworkAnalysisCreate(BaseModel):
    """
    Modelo para validar os dados de uma nova análise antes de serem guardados.
    Não inclui campos gerados pela base de dados como 'id', 'created_at', etc.
    """
    artwork_name: str
    analysis: str
    artist: Optional[str] = None
    year: Optional[str] = None
    style: Optional[str] = None
    emotions: Optional[List[str]] = None
    processing_time: float
    image_hash: Optional[str] = None # Para associar a análise a uma imagem

# ✨✨ FIM DO CÓDIGO ADICIONADO ✨✨

class ArtworkAnalysisResponse(BaseModel):
    """Modelo para a resposta da API ao frontend."""
    id: str = Field(..., description="ID único da análise")
    artwork_name: str = Field(..., description="Nome da obra de arte analisada")
    analysis: str = Field(..., description="Análise detalhada da obra de arte")
    artist: Optional[str] = Field(None, description="Nome do artista")
    year: Optional[str] = Field(None, description="Ano de criação")
    style: Optional[str] = Field(None, description="Estilo artístico")
    emotions: Optional[List[str]] = Field(None, description="Emoções evocadas pela obra")
    processing_time: float = Field(..., description="Tempo de processamento em segundos")
    cached: bool = Field(False, description="Indica se a análise veio do cache")

class ArtworkAnalysisCreate(BaseModel):
    """
    Modelo para validar os dados de uma nova análise antes de serem guardados.
    """
    artwork_name: str
    analysis: str
    artist: Optional[str] = None
    year: Optional[str] = None
    style: Optional[str] = None
    emotions: Optional[List[str]] = None
    processing_time: float
    image_hash: Optional[str] = None

class ArtworkAnalysisDB(BaseModel):
    """Modelo que representa um documento na coleção do MongoDB."""
    artwork_name: str
    analysis: str
    artist: Optional[str] = None
    year: Optional[str] = None
    style: Optional[str] = None
    emotions: Optional[List[str]] = None
    processing_time: float
    image_hash: Optional[str] = Field(None, description="Hash SHA-256 da imagem analisada")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    class Config:
        # Permite que o Pydantic funcione corretamente com os IDs do MongoDB
        from_attributes = True 
        json_encoders = {
            datetime: lambda v: v.isoformat(),
        }