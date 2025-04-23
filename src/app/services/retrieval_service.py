class RetrievalService:
    def __init__(self, db, embedder):
        self.db = db
        self.embedder = embedder

    async def get_relevant_docs(self, query: str, k: int = 5) -> list[str]:
        vec = await self.embedder.embed_query(query)
        rows = await self.db.fetch(
            "SELECT content FROM documents ORDER BY embedding <-> $1 LIMIT $2",
            vec, k
        )
        return [r["content"] for r in rows]
