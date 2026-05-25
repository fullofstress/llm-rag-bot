from sqlalchemy.orm import Session

from services.chunker import TextChunker
from services.embeddings import EmbeddingsService

from models.documents import Document
from models.document_chunks import DocumentChunk

class IngestionService:
    def __init__(self):
        self.chunker = TextChunker()
        self.embedder = EmbeddingsService()

    def ingest_document(self, db: Session, title: str, content: str, source_type: str = "text"):
        doc = Document(
            title=title,
            source_type=source_type,
        )

        db.add(doc)
        db.flush()

        chunks = self.chunker.chunk(content)

        # embed chunks
        embeddings = self.embedder.embed_batch(chunks)

        # store chunks
        for i, (chunk, emb) in enumerate(zip(chunks, embeddings)):
            db.add(DocumentChunk(
                document_id=doc.id,
                content=chunk,
                embedding=emb,
                chunk_index=i,
                meta={"source": source_type},
            ))

        db.commit()
        return doc.id