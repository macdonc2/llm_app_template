from openai import OpenAI
from ..ports.embedding_port import EmbeddingPort
from ..config import settings

class OpenAIEmbeddingAdapter(EmbeddingPort):
    def __init__(self):
        self.client = OpenAI(api_key=settings.openai_api_key)

    async def embed_query(self, text: str) -> list[float]:
        resp = await self.client.embeddings.create(model="text-embedding-3-small", input=text)
        return resp.data[0].embedding
