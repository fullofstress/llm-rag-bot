from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from db import get_db
from services.ingestion import IngestionService
from schemas.admin_ingestion import AdminIngestionRequest

router = APIRouter(prefix="/admin", tags=["admin"])
ingestion_service = IngestionService()

@router.post("/ingestion")
def ingestion(request: AdminIngestionRequest, db: Session = Depends(get_db)):
    results = []

    for doc in request.documents:
        doc_id = ingestion_service.ingest_document(
            db=db,
            title=doc.title,
            content=doc.content,
            source_type=doc.source_type
        )

        results.append({
            "title": doc.title,
            "document_id": doc_id,
            "chunks_created": None
        })

    return {
        "status": True,
        "results": results,
        "ingested_documents": len(results),
    }