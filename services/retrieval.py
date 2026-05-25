from services.embeddings import EmbeddingsService
from sqlalchemy import text
from sqlalchemy.orm import Session

class RetrievalService:
    def __init__(self):
        self.embedder = EmbeddingsService()

    def search(self, db: Session, query: str, top_k: int = 5):
        query_embedding = self.embedder.embed(query)

        query_embedding_str = "[" + ",".join(map(str, query_embedding)) + "]"

        sql = text("""
            SELECT
                id,
                content,
                meta,
                1 - (embedding <=> CAST(:query_embedding AS vector)) AS score
            FROM document_chunks
            ORDER BY embedding <=> CAST(:query_embedding AS vector)
            LIMIT :top_k
        """)

        result = db.execute(sql, {
            "query_embedding": query_embedding_str,
            "top_k": top_k
        })
        return result.fetchall()
