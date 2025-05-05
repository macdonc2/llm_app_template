from typing import List
import httpx

from app.ports.tavily_search_port import TavilySearchPort

class TavilySearchAdapter(TavilySearchPort):
    def __init__(self, base_url: str, api_key: str):
        self.client = httpx.AsyncClient(
            base_url=base_url.rstrip("/"),
            headers={"Authorization": f"Bearer {api_key}"}
        )

    async def search(self, query: str, top_k: int = 5) -> List[str]:
        resp = await self.client.post(
            "/search",
            json={"query": query, "top_k": top_k},
        )
        resp.raise_for_status()
        return resp.json().get("results", [])
