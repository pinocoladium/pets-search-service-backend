from typing import Any

from httpx import AsyncClient


class DjangoHttpClient:
    def __init__(self, base_url: str) -> None:
        self._client = AsyncClient(
            base_url=base_url,
            timeout=10.0,
        )

    async def get(self, url: str) -> Any:
        response = await self._client.get(url)
        response.raise_for_status()
        return response.json()

    async def post(self, url: str, request_data: dict, files: dict | None = None) -> Any:
        response = await self._client.post(url, data=request_data, files=files)
        response.raise_for_status()
        return response.json()

    async def close(self) -> None:
        await self._client.aclose()
