import base64
from typing import Final

import httpx
from django.conf import settings
from django.core.files.images import ImageFile


class OllamaService:
    OLLAMA_BASE_URL: Final[str] = settings.OLLAMA_BASE_URL
    OLLAMA_MODEL: Final[str] = settings.OLLAMA_MODEL

    def generate_response(self, question: str) -> str:
        response = httpx.post(
            f'{self.OLLAMA_BASE_URL}/api/generate',
            json={
                'model': self.OLLAMA_MODEL,
                'system': (
                    'Ты помощник сервиса поиска животных. '
                    'Отвечай только на русском языке. '
                    'Не выдумывай факты, породы, размеры и числа. '
                    'Если данных недостаточно, напиши, что информации недостаточно. '
                    'Если вопрос не касается темы домашних животных, то не отвечай'
                ),
                'prompt': question,
                'stream': False,
                'options': {
                    'temperature': 0.2,
                    'top_p': 0.8,
                },
            },
            timeout=120,
        )
        response.raise_for_status()
        return response.json()['response']

    def describe_image(self, image_file: ImageFile) -> str:
        image_base64 = base64.b64encode(image_file.read()).decode('utf-8')

        response = httpx.post(
            f'{self.OLLAMA_BASE_URL}/api/generate',
            json={
                'model': self.OLLAMA_MODEL,
                'system': (
                    'Ты помощник сервиса поиска животных. '
                    'Опиши животное на фото только на русском языке. '
                    'Не выдумывай факты, которых не видно на изображении. '
                    'Если животное не видно или качество плохое, так и напиши.'
                ),
                'prompt': (
                    'Опиши животное на изображении для объявления. '
                    'Укажи вид животного, цвет, примерный размер, заметные особенности.'
                ),
                'images': [image_base64],
                'stream': False,
                'options': {
                    'temperature': 0.1,
                },
            },
            timeout=180,
        )
        response.raise_for_status()
        return response.json()['response']
