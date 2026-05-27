from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from sqlalchemy.orm import Session

from db import get_db
from services.ingestion import IngestionService
from schemas.admin_ingestion import AdminIngestionRequest
from utils.parser import extract_text_from_pdf, extract_text_from_txt
from services.chunker import TextChunker

router = APIRouter(prefix="/admin", tags=["admin"])
ingestion_service = IngestionService()
chunker = TextChunker()

@router.post("/upload")
async def upload(file: UploadFile = File(...), db: Session = Depends(get_db)):
    filename = file.filename.lower()

    print(filename)

    if filename.endswith(".pdf"):
        text = await extract_text_from_pdf(file)
    elif filename.endswith(".txt"):
        text = await extract_text_from_txt(file)
    else:
        raise HTTPException(status_code=400, detail="Unsupported file type")
    
    results = ingestion_service.ingest_document(
        db=db,
        title=filename,
        content=text,
        source_type=filename.split(".")[-1]
    )

    return {
        "status": True,
        "results": results
    }

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