from typing import Any

import httpx


class HttpClient:
    def __init__(self, base_url: str) -> None:
        self._client = httpx.AsyncClient(
            base_url=base_url,
            timeout=10.0,
        )

    async def get(self, url: str) -> Any:
        response = await self._client.get(url)
        response.raise_for_status()
        return response.json()

    async def close(self) -> None:
        await self._client.aclose()
