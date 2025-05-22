"""
agents_adapter.py

This module provides an adapter class, `AgentsAdapter`, for orchestrating AI-driven 
conversations and tool-invocation over multiple agent control points in a microservices-based 
FastAPI application.

Key Features:
-------------
- Integrates with the OpenAI API for LLM-backed conversational agent tasks.
- Supports dynamic, tool-augmented agent workflows using external MCP (Model Context Protocol) servers 
  via Server-Sent Events (SSE) for real-time tool invocation and results aggregation.
- Designed as an implementation of the AgentPort interface, making it easy to inject and substitute in 
  FastAPI applications via dependency injection.
- Clean abstraction suitable for use in boundary adapters, anti-corruption layers, or orchestrators 
  within a microservices architecture.


Typical Use Case:
-----------------
This adapter is intended to service API endpoints where user queries must be handled by LLM-powered 
agents, which can optionally invoke external tools or microservices for enhanced responses. 
For example, the adapter may be bound to an API route which brokers LLM sessions 
with downstream agent microservices.

Example:
--------
    adapter = AgentsAdapter(
        openai_api_key="YOUR_API_KEY",
        mcp_servers=[MCPServerSse(...), ...],
        instructions="You are a helpful assistant.",
        model="gpt-4o-mini"
    )
    response = await adapter.ask("What is the weather today?")

Dependencies:
-------------
- openai: OpenAI Python SDK for LLM access.
- agents: Custom agent and orchestration classes.
- app.ports.agent_port.AgentPort: Port interface for domain boundary abstraction.

Classes:
--------
- AgentsAdapter: Adapter implementing AgentPort, exposing a coroutine to process queries 
  via a unified conversational agent.

"""

import openai
from typing import List
from agents import Agent, Runner
from agents.mcp import MCPServerSse
from app.ports.agent_port import AgentPort

class AgentsAdapter(AgentPort):
    def __init__(
        self,
        openai_api_key: str,
        mcp_servers: List[object],   # MCPServerSse instances
        instructions: str,
        model: str = "gpt-4o-mini",
    ):
        # configure the OpenAI key for all SDK calls
        openai.api_key = openai_api_key

        # instantiate the Agent, passing in the MCP servers
        self.agent = Agent(
            name="UnifiedAgent",
            instructions=instructions,
            model=model,
            mcp_servers=mcp_servers,
        )

    async def ask(self, query: str) -> str:
        # run the agent; it will invoke tools over SSE as needed
        result = await Runner.run(
            starting_agent=self.agent,
            input=query,
        )
        return result.final_output