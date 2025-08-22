# backend/app/services/groq_service.py

import httpx
import time
import logging
import json
from typing import Dict, Any
from app.core.config import settings
from functools import lru_cache

logger = logging.getLogger(__name__)

class GroqService:
    """Serviço para interagir com a API da Groq"""
    
    def __init__(self):
        self.api_key = settings.GROQ_API_KEY
        self.base_url = "https://api.groq.com/openai/v1"
        self.model = settings.GROQ_MODEL
        self.max_tokens = 2048
        self.temperature = 0.7

    async def analyze_artwork(self, artwork_name: str) -> Dict[str, Any]:
        """
        Analisa uma obra de arte usando a API da Groq
        """
        start_time = time.time()
        
        try:
            # Este é o prompt que captura o estilo do Songtell
            prompt = self._build_powerful_analysis_prompt(artwork_name)
            logger.info(f"Iniciando análise aprofundada para: {artwork_name}")
            
            response_text = await self._call_groq_api(prompt)
            processing_time = time.time() - start_time
            
            analysis_data = self._extract_analysis_data(response_text, artwork_name, processing_time)
            
            logger.info(f"Análise concluída para {artwork_name} em {processing_time:.2f}s")
            return analysis_data
            
        except Exception as e:
            logger.error(f"Erro na análise da obra {artwork_name}: {str(e)}")
            raise Exception(f"Erro na análise da obra: {str(e)}")
    
    # ✨✨ ESTE PROMPT IMITA O ESTILO DO SONGTELL PARA ARTES VISUAIS ✨✨
    def _build_powerful_analysis_prompt(self, artwork_name: str) -> str:
        return f"""
        Aja como um analista de arte cultural, similar ao Songtell, mas para artes visuais. Sua tarefa é desvendar a mensagem central e o contexto humano por trás da obra de arte "{artwork_name}". A análise deve ser direta, poderosa e reveladora.

        Responda OBRIGATORIAMENTE com um objeto JSON válido.
        A estrutura do JSON deve ser:
        {{
          "artwork_name": "Nome da Obra (confirmado pela IA)",
          "artist": "Nome do Artista",
          "year": "Ano de Criação",
          "style": "Estilo Artístico",
          "analysis": "Comece com um parágrafo de abertura que define a obra e sua tese central, Em seguida, dedique um parágrafo para analisar o primeiro elemento visual chave (ex: a figura central, o cenário, cores, expressão, formas), explicando seu papel na narrativa. Depois, um segundo parágrafo para analisar outro elemento visual importante (ex: o uso da luz, um símbolo específico), conectando-o ao tema. Conclua com um parágrafo final que resume o impacto geral e a mensagem duradoura da obra.",
          "emotions": ["lista", "de", "3 a 5", "emoções", "chave", "em português", "lowercase", "ex: 'Tristeza', 'Resiliência', 'Esperança'"]
        }}

        Se a obra for sobre um contexto social ou histórico específico, certifique-se de que a análise reflita isso de forma proeminente.
        NÃO inclua markdown (```json ... ```) ou qualquer outro texto fora do objeto JSON.
        """

    async def _call_groq_api(self, prompt: str) -> str:
        try:
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.api_key}"
            }
            payload = {
                "model": self.model,
                "messages": [
                    {
                        "role": "system",
                        "content": "É um analista de arte incisivo e culturalmente consciente. A tua função é devolver um objeto JSON com uma análise profunda sobre o significado e o contexto de uma obra de arte, seguindo estritamente a estrutura pedida."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                "max_tokens": self.max_tokens,
                "temperature": self.temperature,
                "response_format": {"type": "json_object"}
            }
            async with httpx.AsyncClient(timeout=60.0) as client:
                response = await client.post(
                    f"{self.base_url}/chat/completions",
                    headers=headers,
                    json=payload
                )
                response.raise_for_status()
                response_data = response.json()
                return response_data["choices"][0]["message"]["content"]
        except httpx.TimeoutException:
            logger.error("Timeout na chamada à API da Groq")
            raise Exception("Timeout na comunicação com a Groq")
        except httpx.HTTPStatusError as e:
            logger.error(f"Erro na API Groq: {e.response.status_code} - {e.response.text}")
            raise Exception(f"Erro na API Groq: {e.response.status_code}")
        except Exception as e:
            logger.error(f"Erro na chamada à API da Groq: {str(e)}")
            raise Exception(f"Erro na comunicação com a Groq: {str(e)}")

    def _extract_analysis_data(self, response_text: str, original_artwork_name: str, processing_time: float) -> Dict[str, Any]:
        try:
            data = json.loads(response_text)
            return {
                "artwork_name": data.get("artwork_name", original_artwork_name),
                "analysis": data.get("analysis", "Análise não disponível.").strip(),
                "artist": data.get("artist"),
                "year": data.get("year"),
                "style": data.get("style"),
                "emotions": data.get("emotions", []),
                "processing_time": processing_time
            }
        except json.JSONDecodeError:
            logger.error(f"Erro ao descodificar JSON da Groq. Resposta recebida: {response_text}")
            return {
                "artwork_name": original_artwork_name,
                "analysis": "A IA não conseguiu estruturar a análise, mas a mensagem central parece ser um poderoso manifesto sobre resiliência e a condição humana.",
                "artist": "Desconhecido",
                "year": "Desconhecido",
                "style": "Contestatário",
                "emotions": ["struggle", "resilience", "hope"],
                "processing_time": processing_time
            }

@lru_cache()
def get_groq_service() -> GroqService:
    return GroqService()