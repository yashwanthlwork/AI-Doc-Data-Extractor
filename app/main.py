from fastapi import FastAPI,UploadFile,File

app=FastAPI(
    title="Inteliggence Document Processing",
    description="Extrcating required data from Documents Using LLM ",
    version="0.0.1"
)

@app.get("/")

def root():
    return{
        "status":"running"
    }

@app.post("/upload")

def upload_file(file: UploadFile = File(...)):
    return{
        "filename":file.filename,
        "Content-type":file.content_type
    }
