import httpx
import time
import logging
from typing import Dict, Any
from app.core.config import settings

logger = logging.getLogger(__name__)

class GroqService:
    """Serviço para interagir com a API da Groq"""
    
    def __init__(self):
        """Inicializa o cliente Groq com a chave da API"""
        self.api_key = settings.GROQ_API_KEY
        self.base_url = "https://api.groq.com/openai/v1"
        self.model = settings.GROQ_MODEL
        self.max_tokens = settings.GROQ_MAX_TOKENS
        self.temperature = settings.GROQ_TEMPERATURE
    
    async def analyze_artwork(self, artwork_name: str) -> Dict[str, Any]:
        """
        Analisa uma obra de arte usando a API da Groq
        
        Args:
            artwork_name: Nome da obra de arte a ser analisada
            
        Returns:
            Dicionário com a análise da obra de arte
        """
        start_time = time.time()
        
        try:
            # Construir prompt detalhado para análise de arte
            prompt = self._build_analysis_prompt(artwork_name)
            
            logger.info(f"Iniciando análise da obra: {artwork_name}")
            
            # Chamar API da Groq
            response = await self._call_groq_api(prompt)
            
            # Calcular tempo de processamento
            processing_time = time.time() - start_time
            
            # Extrair e processar resposta
            analysis_data = self._extract_analysis_data(response, artwork_name, processing_time)
            
            logger.info(f"Análise concluída para {artwork_name} em {processing_time:.2f}s")
            
            return analysis_data
            
        except Exception as e:
            logger.error(f"Erro na análise da obra {artwork_name}: {str(e)}")
            raise Exception(f"Erro na análise da obra: {str(e)}")
    
    def _build_analysis_prompt(self, artwork_name: str) -> str:
        """
        Constrói um prompt detalhado para análise de arte
        
        Args:
            artwork_name: Nome da obra de arte
            
        Returns:
            Prompt formatado para a API da Groq
        """
        return f"""
        Analisa a obra de arte "{artwork_name}" e fornece uma análise detalhada e informativa.
        
        A tua análise deve incluir:
        
        1. **Contexto Histórico**: Período, movimento artístico e contexto cultural
        2. **Análise Técnica**: Técnicas utilizadas, composição, uso de cores e formas
        3. **Significado e Interpretação**: O que a obra representa e comunica
        4. **Influências e Legado**: Impacto na história da arte e influências
        5. **Emoções Evocadas**: Que sentimentos e emoções a obra transmite
        
        Responde em português de forma clara, educativa e envolvente.
        Se não conseguires identificar a obra específica, fornece uma análise geral baseada no nome.
        
        Formato da resposta: texto contínuo e bem estruturado, sem listas ou títulos.
        """
    
    async def _call_groq_api(self, prompt: str) -> str:
        """
        Chama a API da Groq usando httpx
        
        Args:
            prompt: Prompt para enviar à API
            
        Returns:
            Resposta da API da Groq
        """
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
                        "content": "És um especialista em história da arte com conhecimento profundo sobre obras de arte, artistas e movimentos artísticos. Forneces análises detalhadas, educativas e envolventes."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                "max_tokens": self.max_tokens,
                "temperature": self.temperature
            }
            
            async with httpx.AsyncClient(timeout=60.0) as client:
                response = await client.post(
                    f"{self.base_url}/chat/completions",
                    headers=headers,
                    json=payload
                )
                
                if response.status_code != 200:
                    error_msg = f"Erro na API Groq: {response.status_code} - {response.text}"
                    logger.error(error_msg)
                    raise Exception(error_msg)
                
                response_data = response.json()
                return response_data["choices"][0]["message"]["content"]
                
        except httpx.TimeoutException:
            logger.error("Timeout na chamada à API da Groq")
            raise Exception("Timeout na comunicação com a Groq")
        except Exception as e:
            logger.error(f"Erro na chamada à API da Groq: {str(e)}")
            raise Exception(f"Erro na comunicação com a Groq: {str(e)}")
    
    def _extract_analysis_data(self, response: str, artwork_name: str, processing_time: float) -> Dict[str, Any]:
        """
        Extrai e estrutura os dados da análise
        
        Args:
            response: Resposta da API da Groq
            artwork_name: Nome da obra de arte
            processing_time: Tempo de processamento
            
        Returns:
            Dicionário estruturado com os dados da análise
        """
        # Por enquanto, retornamos a análise como texto simples
        # Em versões futuras, podemos implementar parsing mais sofisticado
        return {
            "artwork_name": artwork_name,
            "analysis": response.strip(),
            "artist": None,  # Será implementado com parsing mais avançado
            "year": None,    # Será implementado com parsing mais avançado
            "style": None,   # Será implementado com parsing mais avançado
            "emotions": [],  # Será implementado com parsing mais avançado
            "processing_time": processing_time
        }

@lru_cache()
def get_groq_service() -> GroqService:
    return GroqService()