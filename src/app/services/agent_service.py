from app.ports.agent_port import AgentPort

class AgentService:
    def __init__(self, adapter: AgentPort):
        self.adapter = adapter

    async def ask(self, query: str) -> str:
        return await self.adapter.ask(query)
