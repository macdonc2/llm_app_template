"""
tavily_search_adapter.py

This module implements an adapter for interfacing with the external Tavily search service in a microservices-based FastAPI application. It provides asynchronous HTTP client capabilities using httpx, encapsulating all remote search logic behind a clean interface conforming to the `TavilySearchPort`.

Overview:
---------
The `TavilySearchAdapter` class abstracts the details of communicating with the Tavily search API, enabling other microservice components to perform external queries without knowledge of HTTP handling or authentication. This follows the ports-and-adapters (hexagonal) architecture, promoting loose coupling and easy replacement of external dependencies.

Key Features:
-------------
- **Async HTTP Integration:** Utilizes httpx.AsyncClient to perform non-blocking communication for scalable microservices.
- **Configurable Timeouts:** Defines granular connection/read/write/pool timeouts to gracefully handle slow or unreliable network conditions typical in distributed systems.
- **Robust Error Handling:** Implements automatic retries with exponential backoff for resilient querying of third-party APIs. Propagates persistent errors to allow the microservice to respond appropriately.
- **Security:** Automatically annotates HTTP requests with the API key in the Authorization header.
- **Clean Abstraction:** Exposes only a simple `search` interface, hiding all HTTP-specific logic from the rest of the application.

Key Methods:
------------
- **search(query: str, top_k: int = 5) -> List[str]:**
    - Takes a user query and the desired number of top results. Returns a list of result strings from Tavily, or an empty list if none found.
    - Retries up to 5 times on transient errors, with a capped exponential backoff delay.

Intended Usage:
---------------
Intended to be injected into FastAPI routes, service layers, or background workers that require external semantic search capabilities. By limiting communication concerns to this adapter, the rest of the microservice remains decoupled and easy to test.

Dependencies:
-------------
- httpx (for async HTTP)
- asyncio (for concurrency, backoff)
- Project-specific search port interface

"""

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
