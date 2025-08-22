# backend/app/core/utils.py

import hashlib
import base64

def generate_image_hash(image_data: bytes) -> str:
    """
    Gera um hash SHA-256 para os dados de uma imagem para ser usado como
    um identificador único no sistema de cache.
    """
    return hashlib.sha256(image_data).hexdigest()

def image_to_base64(image_data: bytes) -> str:
    """
    Converte os dados binários de uma imagem para uma string no formato base64.
    Isto é necessário para enviar a imagem para a API de IA dentro de um JSON.
    """
    return base64.b64encode(image_data).decode('utf-8')