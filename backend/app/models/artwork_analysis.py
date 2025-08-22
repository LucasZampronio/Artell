# backend/app/models/artwork_analysis.py
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime

class ArtworkAnalysisRequest(BaseModel):
    """Modelo para requisição de análise de obra de arte por nome"""
    artwork_name: str = Field(
        ..., 
        description="Nome da obra de arte a ser analisada",
        min_length=1,
        max_length=200,
        example="A Noite Estrelada"
    )

class ArtworkAnalysisResponse(BaseModel):
    """Modelo para resposta de análise de obra de arte"""
    id: str = Field(..., description="ID único da análise") # Adicionado para suportar navegação
    artwork_name: str = Field(..., description="Nome da obra de arte analisada") # Alterado de 'artwork' para 'artwork_name'
    analysis: str = Field(..., description="Análise detalhada da obra de arte")
    artist: Optional[str] = Field(None, description="Nome do artista (se identificado)")
    year: Optional[str] = Field(None, description="Ano de criação (se identificado)")
    style: Optional[str] = Field(None, description="Estilo artístico (se identificado)")
    emotions: Optional[List[str]] = Field(None, description="Emoções evocadas pela obra")
    processing_time: float = Field(..., description="Tempo de processamento em segundos")
    cached: bool = Field(False, description="Indica se a análise veio do cache")

class ArtworkAnalysisDB(BaseModel):
    """Modelo para armazenar análise na base de dados"""
    artwork_name: str = Field(..., description="Nome da obra de arte")
    analysis: str = Field(..., description="Análise detalhada da obra de arte")
    artist: Optional[str] = Field(None, description="Nome do artista")
    year: Optional[str] = Field(None, description="Ano de criação")
    style: Optional[str] = Field(None, description="Estilo artístico")
    emotions: Optional[List[str]] = Field(None, description="Emoções evocadas")
    processing_time: float = Field(..., description="Tempo de processamento")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }
