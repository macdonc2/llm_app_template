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