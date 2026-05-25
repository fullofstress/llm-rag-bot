from pydantic import BaseModel
from typing import List, Optional

class DocumentIngetionItem(BaseModel):
    title: str
    content: str
    source_type: str = "text"

class AdminIngestionRequest(BaseModel):
    documents: List[DocumentIngetionItem]