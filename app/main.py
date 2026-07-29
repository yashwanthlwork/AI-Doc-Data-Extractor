from fastapi import FastAPI,UploadFile,File
from app.Services.documentservice import DocumentService


app=FastAPI(
    title="Inteligence Document Processing",
    description="Extrcating required data from Documents Using LLM ",
    version="0.0.1"
)

@app.get("/")

def root():
    return{
        "status":"running"
    }

@app.post("/upload")

async def upload_file(file: UploadFile = File(...)):
    pdf_bytes=await file.read()
    documentservice=DocumentService()
    documentservice.upload_document(file.filename,pdf_bytes)
    return{
        "filename":file.filename,
        "Content-type":file.content_type
    }
