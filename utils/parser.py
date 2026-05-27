from pypdf import PdfReader
from io import BytesIO
import asyncio

async def extract_text_from_pdf(file):
    content = await file.read()
    pdf_stream = BytesIO(content)

    reader = PdfReader(pdf_stream)
    text = ""

    for page in reader.pages:
        text += page.extract_text()
    return text

def extract_text_from_txt(file):
    return file.read().decode("utf-8")