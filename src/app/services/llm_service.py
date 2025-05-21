from app.ports.llm_port import LLMPort

class LLMService:
    """
    Service class for interacting with a large language model (LLM) adapter.

    This class provides methods to communicate with the underlying LLM for generating responses.

    Attributes:
        llm (LLMPort): The LLM adapter instance used for communication.

    Methods:
        chat(prompt: str) -> str:
            Asynchronously generate a response from the LLM based on the provided prompt.
    """

    def __init__(self, llm: LLMPort):
        """
        Initialize the LLMService with a specific LLM adapter.

        Args:
            llm (LLMPort): The LLM adapter instance.
        """

        self.llm = llm

    async def chat(self, prompt: str) -> str:
        """
        Asynchronously generate a response from the LLM.

        Args:
            prompt (str): The input prompt to send to the LLM.

        Returns:
            str: The generated response from the LLM.
        """
        
        return await self.llm.chat(prompt)
