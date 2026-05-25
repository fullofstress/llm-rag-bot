from sqlalchemy import Column, Index, Text, UUID, ForeignKey, DateTime, Integer, DDL, event
from uuid import uuid4
from datetime import datetime
from pgvector.sqlalchemy import Vector
from sqlalchemy.dialects.postgresql import JSONB, TSVECTOR

EMBEDDING_DIM = 384
from models.base import Base

class DocumentChunk(Base):
    __tablename__ = "document_chunks"
    id = Column(UUID, primary_key=True, default=uuid4)
    document_id = Column(UUID, ForeignKey("documents.id"), nullable=False)
    content = Column(Text, nullable=False)

    # pgvector embedding
    embedding = Column(Vector(EMBEDDING_DIM), nullable=False)

    chunk_index = Column(Integer, nullable=False)
    token_count = Column(Integer, nullable=True)

    meta = Column(JSONB, default={})    

    content_tsv = Column(TSVECTOR, nullable=True)

    created_at = Column(DateTime, default=datetime.now)

    __table_args__ = (
        Index("idx_document_chunks_document_id", "document_id"),
        Index("idx_chunks_metadata", "meta", postgresql_using="gin"),
        Index(
            "idx_chunks_embedding_vector", 
            "embedding", 
            postgresql_using="hnsw", 
            postgresql_ops={"embedding": "vector_cosine_ops"}
        ),
        Index("idx_chunks_content_tsv", "content_tsv", postgresql_using="gin"),
    )

create_trigger_sql = """
CREATE FUNCTION update_tsv() RETURNS trigger AS $$
BEGIN
  NEW.content_tsv := to_tsvector('english', NEW.content);
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER tsv_update
BEFORE INSERT OR UPDATE ON document_chunks
FOR EACH ROW EXECUTE FUNCTION update_tsv();
"""

drop_trigger_sql = """
DROP TRIGGER IF EXISTS tsv_update ON document_chunks;
DROP FUNCTION IF EXISTS update_tsv();
"""

# Attach the trigger creation code to the table creation event lifecycle
event.listen(
    DocumentChunk.__table__,
    "after_create",
    DDL(create_trigger_sql)
)

# Attach the trigger removal code to the table destruction event lifecycle
event.listen(
    DocumentChunk.__table__,
    "before_drop",
    DDL(drop_trigger_sql)
)