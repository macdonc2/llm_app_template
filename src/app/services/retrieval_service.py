class RetrievalService:
    """
    Service class for retrieving relevant documents based on query embeddings.

    This class handles interaction between a database and an embedding provider
    to fetch documents most relevant to a user's query.

    Attributes:
        db: The database instance for document retrieval.
        embedder: The embedding provider used to generate vector representations of queries.

    Methods:
        get_relevant_docs(query: str, k: int = 5) -> list[str]:
            Asynchronously fetch the top-k most relevant documents for a given query.
    """

    def __init__(self, db, embedder):
        """
        Initialize the RetrievalService with a database and an embedding provider.

        Args:
            db: The database instance for retrieving documents.
            embedder: The embedding provider instance for generating embeddings.
        """

        self.db = db
        self.embedder = embedder

    async def get_relevant_docs(self, query: str, k: int = 5) -> list[str]:
        """
        Retrieve the top-k most relevant documents for the provided query.

        Args:
            query (str): The user's search query.
            k (int, optional): The number of top results to return. Defaults to 5.

        Returns:
            list[str]: A list of the most relevant document contents.
        """
        
        vec = await self.embedder.embed_query(query)
        rows = await self.db.fetch(
            "SELECT content FROM documents ORDER BY embedding <-> $1 LIMIT $2",
            vec, k
        )
        return [r["content"] for r in rows]
