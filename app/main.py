from fastapi import FastAPI,UploadFile,File,HTTPException
from pydantic import BaseModel
from app.Services.documentservice import DocumentService
from app.Services.pageservice import PageService
from app.Services.documenttypeservice import DocumentTypeService
from app.Services.promptservice import PromptService
from app.Services.documentclassificationservice import DocumentClassificationService
from app.Services.documentdataextractionservice import DocumentDataExtractionService
from uuid import UUID


class PromptUpdate(BaseModel):
    prompt: str | None = None
    document_type_id: UUID | None = None

app=FastAPI(
    title="AI Document Intelligence API",
    description="""
An AI-powered backend application for processing PDF documents through
document upload, page generation, markdown extraction, document
classification, and structured data extraction.
""",
    version="1.0.0"
)

@app.get("/")

def root():
    return{
        "status":"running"
    }

@app.post("/documents")

async def upload_file(file: UploadFile = File(...)):
    pdf_bytes=await file.read()
    documentservice=DocumentService()
    try:
        document_id=documentservice.upload_document(file.filename,pdf_bytes)
        return{
            "filename":file.filename,
            "Content_type":file.content_type,
            "document_id":str(document_id)
        }
    except ValueError as ex:
        raise HTTPException(
            status_code=409,
            detail=str(ex)
        )

@app.post("/documents/{document_id}/pages")

def create_pages(document_id: UUID):
    page_service = PageService()
    page_service.upload_pages(document_id)

    return {
        "document_id": document_id,
        "status": "PAGES_CREATED"
    }

@app.post("/documents/{document_id}/markdown")

def extract_markdown(document_id: UUID):
    page_service=PageService()
    page_service.extract_markdown(document_id)
    return {
            "document_id": document_id,
            "status": "MARKDOWN_EXTRACTED"
        }

@app.post("/documents/{document_id}/extracted-data")

def extract_data(document_id: UUID):
    service = DocumentDataExtractionService()
    return service.extract_data(document_id)

@app.post("/document-types")

def create_document_type(document_type_name:str,document_type_description:str):
    service=DocumentTypeService()
    try:
        return service.create_document_type(
            document_type_name,
            document_type_description
        )
    except ValueError as ex:
        raise HTTPException(
            status_code=400,
            detail=str(ex)
        )
    
@app.get("/document-types")

def get_all_document_types():
    service=DocumentTypeService()
    return service.get_all_document_types()

@app.post("/documents/{document_id}/classification")

def classify_document(document_id:UUID):
    document_classification_service=DocumentClassificationService()
    document_type = document_classification_service.classify_document(document_id)
    return document_type

@app.post("/prompts")

def create_prompt(prompt_name:str,prompt:str,document_type_id):
    promptservice=PromptService()
    prompt_creation=promptservice.create_prompt(prompt_name,prompt,document_type_id)
    return prompt_creation

@app.get("/prompts")

def fetch_all_prompts():
    promptservice=PromptService()
    all_prompt=promptservice.fetch_all_prompts()
    return all_prompt

@app.patch("/prompts/{prompt_id}")
def update_prompt(prompt_id: UUID, data: PromptUpdate):
    promptservice = PromptService()

    return promptservice.update_prompt(
        prompt_id,
        data.prompt,
        data.document_type_id
    )