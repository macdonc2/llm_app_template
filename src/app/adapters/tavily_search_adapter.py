import asyncio
from typing import List
from httpx import AsyncClient, HTTPError, Timeout

from app.ports.tavily_search_port import TavilySearchPort

class TavilySearchAdapter(TavilySearchPort):
    def __init__(self, base_url: str, api_key: str):
        timeout = Timeout(
            connect=10.0,  
            read=60.0,     
            write=30.0,    
            pool=5.0       
        )
        self.client = AsyncClient(
            base_url=base_url.rstrip("/"),
            headers={"Authorization": f"Bearer {api_key}"},
            timeout=timeout,
        )

    async def search(self, query: str, top_k: int = 5) -> List[str]:
        max_tries = 5
        for attempt in range(max_tries):
            try:
                resp = await self.client.post(
                    "/search",
                    json={"query": query, "max_results": top_k},
                )
                if resp.status_code != 200:
                    body = await resp.text()
                    print(f"Tavily  error {resp.status_code}: {body}")
                resp.raise_for_status()
                data = resp.json()
                # return the `results` list, or empty if missing
                return data.get("results", [])
            except (HTTPError, asyncio.TimeoutError):
                # if last attempt, re-raise so caller sees the error
                if attempt == max_tries - 1:
                    raise
                # otherwise back off and retry
                backoff = min(2 ** attempt, 8)
                await asyncio.sleep(backoff)
