from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from enum import Enum

class AnalysisType(str, Enum):
    IMAGE = "image"
    TEXT = "text"

class ArtworkStyle(str, Enum):
    RENAISSANCE = "renaissance"
    BAROQUE = "baroque"
    IMPRESSIONISM = "impressionism"
    EXPRESSIONISM = "expressionism"
    CUBISM = "cubism"
    SURREALISM = "surrealism"
    ABSTRACT = "abstract"
    CONTEMPORARY = "contemporary"
    OTHER = "other"

class Emotion(str, Enum):
    JOY = "joy"
    SADNESS = "sadness"
    ANGER = "anger"
    FEAR = "fear"
    SURPRISE = "surprise"
    DISGUST = "disgust"
    CONTEMPT = "contempt"
    LOVE = "love"
    PEACE = "peace"
    EXCITEMENT = "excitement"
    MELANCHOLY = "melancholy"
    AWE = "awe"
    OTHER = 'other'

class AnalysisRequest(BaseModel):
    """Modelo para requisições de análise"""
    artwork_name: Optional[str] = Field(None, description="Nome da obra de arte (para análise por texto)")
    analysis_type: AnalysisType = Field(..., description="Tipo de análise (imagem ou texto)")

class AnalysisResponse(BaseModel):
    """Modelo para respostas de análise"""
    id: str = Field(..., description="ID único da análise")
    artwork_name: str = Field(..., description="Nome da obra de arte")
    artist_name: Optional[str] = Field(None, description="Nome do artista")
    year_created: Optional[str] = Field(None, description="Ano de criação")
    style: Optional[ArtworkStyle] = Field(None, description="Estilo artístico")
    
    # Análise da IA
    meaning: str = Field(..., description="Significado e interpretação da obra")
    artist_intention: str = Field(..., description="Intenção do artista")
    emotions: List[Emotion] = Field(..., description="Emoções evocadas pela obra")
    emotional_description: str = Field(..., description="Descrição detalhada das emoções")
    
    # Metadados
    analysis_type: AnalysisType = Field(..., description="Tipo de análise realizada")
    image_hash: Optional[str] = Field(None, description="Hash da imagem (para cache)")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    processing_time: float = Field(..., description="Tempo de processamento em segundos")
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }

class AnalysisCreate(BaseModel):
    """Modelo para criação de análise"""
    artwork_name: str
    artist_name: Optional[str] = None
    year_created: Optional[str] = None
    style: Optional[ArtworkStyle] = None
    meaning: str
    artist_intention: str
    emotions: List[Emotion]
    emotional_description: str
    analysis_type: AnalysisType
    image_hash: Optional[str] = None
    processing_time: float

class AnalysisList(BaseModel):
    """Modelo para listagem de análises"""
    analyses: List[AnalysisResponse]
    total: int
    page: int
    limit: int
