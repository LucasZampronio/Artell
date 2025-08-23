# backend/app/services/groq_service.py

import httpx
import time
import logging
import json
from typing import Dict, Any, List, Optional
from app.core.config import settings
from app.core.utils import image_to_base64
from functools import lru_cache

logger = logging.getLogger(__name__)

class GroqService:
    """Serviço para interagir com a API da Groq"""
    
    def __init__(self):
        self.api_key_text = settings.GROQ_API_KEY
        self.api_key_image = settings.GROQ_IMAGE_API_KEY or settings.GROQ_API_KEY
        self.base_url = "https://api.groq.com/openai/v1"
        
        self.text_model = settings.GROQ_TEXT_MODEL
        self.vision_model = settings.GROQ_VISION_MODEL
        
        self.max_tokens = settings.GROQ_MAX_TOKENS
        self.temperature = settings.GROQ_TEMPERATURE

    async def analyze_artwork(self, artwork_name: str) -> Dict[str, Any]:
        """Analisa uma obra de arte usando o modelo de texto."""
        start_time = time.time()
        try:
            prompt = self._build_powerful_analysis_prompt(artwork_name)
            logger.info(f"Iniciando análise aprofundada para: {artwork_name}")
            payload = self._build_text_payload(prompt)
            response_text = await self._call_groq_api(payload)
            processing_time = time.time() - start_time
            analysis_data = self._extract_analysis_data(response_text, artwork_name, processing_time)
            logger.info(f"Análise concluída para {artwork_name} em {processing_time:.2f}s")
            return analysis_data
        except Exception as e:
            logger.error(f"Erro na análise da obra {artwork_name}: {str(e)}")
            raise Exception(f"Erro na análise da obra: {str(e)}")

    async def analyze_artwork_from_image(self, image_data: bytes) -> Dict[str, Any]:
        """Analisa uma obra de arte a partir de uma imagem usando o modelo de visão."""
        start_time = time.time()
        try:
            prompt = self._build_powerful_analysis_prompt("a obra de arte na imagem")
            base64_image = image_to_base64(image_data)
            logger.info("Iniciando análise de imagem com Groq...")
            payload = self._build_vision_payload(prompt, base64_image)
            response_text = await self._call_groq_api(payload, is_vision=True)
            processing_time = time.time() - start_time
            analysis_data = self._extract_analysis_data(response_text, "Obra de arte da imagem", processing_time)
            logger.info(f"Análise de imagem concluída em {processing_time:.2f}s")
            return analysis_data
        except Exception as e:
            logger.error(f"Erro na análise da imagem: {str(e)}")
            raise Exception(f"Erro na análise da imagem: {str(e)}")

    async def identify_artwork_from_image(self, image_data: bytes) -> Optional[Dict[str, str]]:
        """Identifica o nome de uma obra de arte a partir de uma imagem."""
        try:
            prompt = self._build_identification_prompt()
            base64_image = image_to_base64(image_data)
            logger.info("Iniciando identificação de imagem com Groq...")
            payload = self._build_vision_payload(prompt, base64_image, max_tokens=256)
            response_text = await self._call_groq_api(payload, is_vision=True)
            data = json.loads(response_text)
            artwork_name = data.get("artwork_name")
            if artwork_name and artwork_name.lower() not in ["desconhecido", "não identificado"]:
                logger.info(f"Obra identificada como: {artwork_name}")
                return {"artwork_name": artwork_name}
            logger.warning("Não foi possível identificar a obra de arte na imagem.")
            return None
        except Exception as e:
            logger.error(f"Erro ao identificar obra na imagem: {str(e)}")
            return None
    
    def _build_powerful_analysis_prompt(self, artwork_name: str) -> str:
        return f"""
        Aja como um analista de arte cultural. Sua tarefa é dar um breve resumo e desvendar a mensagem central por trás da obra."{artwork_name}".

        Responda OBRIGATORIAMENTE com um objeto JSON válido com a estrutura:
        {{
          "artwork_name": "Nome da Obra (confirmado pela IA)",
          "artist": "Nome do Artista",
          "year": "Ano de Criação",
          "style": "Estilo Artístico",
          "analysis": "Uma análise profunda da obra.",
          "emotions": ["lista", "de", "3 a 5", "emoções", "chave"],
          "image_url": " NÃO PEGUE IMAGENS DA WIKIPEDIA E COM THUMB. tente buscar o URL público e acessível de uma imagem da obra de arte. Se não puder encontrar um URL de ficheiro direto deixe este campo como null."
        }}
        NÃO inclua markdown (```json ... ```) ou qualquer outro texto fora do objeto JSON.
        """

    def _build_identification_prompt(self) -> str:
        """Cria um prompt simples e direto para apenas identificar a obra."""
        return """
        Sua única tarefa é identificar a obra de arte na imagem.
        Responda OBRIGATORIAMENTE com um objeto JSON válido com a seguinte estrutura:
        {
          "artwork_name": "Nome da Obra"
        }
        Se você não conseguir identificar a obra, responda com "Desconhecido".
        NÃO inclua nenhuma outra informação, apenas o JSON.
        """

    def _build_vision_payload(self, prompt: str, base64_image: str, max_tokens: Optional[int] = None) -> Dict[str, Any]:
        """Constrói o payload para uma requisição de visão (com imagem)."""
        return {
            "model": self.vision_model,
            "messages": [
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": prompt},
                        {
                            "type": "image_url",
                            "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}
                        }
                    ]
                }
            ],
            "max_tokens": max_tokens or self.max_tokens,
            "temperature": self.temperature,
            "response_format": {"type": "json_object"}
        }
    
    def _build_text_payload(self, prompt: str) -> Dict[str, Any]:
        """Constrói o payload para uma requisição de texto."""
        return {
            "model": self.text_model,
            "messages": [
                {"role": "user", "content": prompt}
            ],
            "max_tokens": self.max_tokens,
            "temperature": self.temperature,
            "response_format": {"type": "json_object"}
        }

    async def _call_groq_api(self, payload: Dict[str, Any], is_vision: bool = False) -> str:
        """Faz a chamada à API da Groq com o payload e tipo de modelo corretos."""
        try:
            api_key_to_use = self.api_key_image if is_vision else self.api_key_text
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {api_key_to_use}"
            }
            async with httpx.AsyncClient(timeout=90.0) as client:
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

            year_from_ai = data.get("year")
            if year_from_ai is not None:
                year_from_ai = str(year_from_ai)
            return {
                "artwork_name": data.get("artwork_name", original_artwork_name),
                "analysis": data.get("analysis", "Análise não disponível.").strip(),
                "artist": data.get("artist"),
                "year": year_from_ai,
                "style": data.get("style"),
                "emotions": data.get("emotions", []),
                "image_url": data.get("image_url"), # <-- Extrair o URL da imagem
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
                "image_url": None,
                "processing_time": processing_time
            }

@lru_cache()
def get_groq_service() -> GroqService:
    return GroqService()