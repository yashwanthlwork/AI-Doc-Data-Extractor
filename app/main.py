from fastapi import FastAPI,UploadFile,File,HTTPException
from app.Services.documentservice import DocumentService
from app.Services.pageservice import PageService
from app.Services.documenttypeservice import DocumentTypeService
from app.Services.documentclassificationservice import DocumentClassificationService

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
    document_id=documentservice.upload_document(file.filename,pdf_bytes)
    return{
        "filename":file.filename,
        "Content_type":file.content_type,
        "document_id":str(document_id)
    }

@app.post("/documents/{document_id}/create-pages")

def create_pages(document_id: str):
    page_service = PageService()
    page_service.upload_pages(document_id)

    return {
        "document_id": document_id,
        "status": "PAGES_CREATED"
    }

@app.post("/documents/{document_id}/extract-markdown")

def extract_markdown(document_id: str):
    page_service=PageService()
    page_service.extract_markdown(document_id)
    return {
            "document_id": document_id,
            "status": "MARKDOWN_EXTRACTED"
        }

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

@app.post("/classify-document")
def classify_document(document_id:str):
    service=DocumentClassificationService()
    return service.classify_document(document_id)

