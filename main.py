from fastapi import FastAPI

#creating the app
app=FastAPI(
    Title="AI Doc Intelligence",
    Tag="1.0.0"
)

@app.get("/")
def home():
    return {"message":"Welcome to AI Doc Intelligence"}