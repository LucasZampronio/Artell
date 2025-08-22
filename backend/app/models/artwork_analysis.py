# backend/app/models/artwork_analysis.py

from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime

class ArtworkAnalysisRequest(BaseModel):
    """Modelo para requisição de análise de obra de arte por nome."""
    artwork_name: str = Field(..., min_length=1, max_length=200)

class ArtworkAnalysisCreate(BaseModel):
    """Modelo para validar os dados de uma nova análise antes de serem guardados."""
    artwork_name: str
    analysis: str
    artist: Optional[str] = None
    year: Optional[str] = None
    style: Optional[str] = None
    emotions: Optional[List[str]] = None
    processing_time: float
    image_hash: Optional[str] = None
    image_url: Optional[str] = None

class ArtworkAnalysisResponse(BaseModel):
    """Modelo para a resposta da API ao frontend."""
    id: str = Field(..., description="ID único da análise")
    artwork_name: str
    analysis: str
    artist: Optional[str] = None
    year: Optional[str] = None
    style: Optional[str] = None
    emotions: Optional[List[str]] = None
    processing_time: float
    cached: bool = False
    image_url: Optional[str] = None

class ArtworkAnalysisDB(BaseModel):
    """Modelo que representa um documento na coleção do MongoDB."""
    artwork_name: str
    analysis: str
    artist: Optional[str] = None
    year: Optional[str] = None
    style: Optional[str] = None
    emotions: Optional[List[str]] = None
    processing_time: float
    image_hash: Optional[str] = None
    image_url: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        from_attributes = True
        json_encoders = { datetime: lambda v: v.isoformat() }