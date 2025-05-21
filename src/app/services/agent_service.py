from app.ports.agent_port import AgentPort

class AgentService:
    """
    Service class for interacting with an agent adapter.

    This class provides a high-level interface for processing queries via the agent.

    Attributes:
        adapter (AgentPort): The agent adapter used to handle queries.

    Methods:
        ask(query: str) -> str:
            Asynchronously process a query using the agent adapter and return the response.
    """

    def __init__(self, adapter: AgentPort):
        """
        Initialize the AgentService with a specific agent adapter.

        Args:
            adapter (AgentPort): The agent adapter instance.
        """

        self.adapter = adapter

    async def ask(self, query: str) -> str:
        """
        Submit a query to the agent and retrieve the response.

        Args:
            query (str): The query string to process.

        Returns:
            str: The agent's response to the query.
        """
        
        return await self.adapter.ask(query)
