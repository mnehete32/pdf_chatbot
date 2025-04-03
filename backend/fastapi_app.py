from fastapi import FastAPI, Request, Form
from fastapi.responses import JSONResponse
import threading
import os
import time
import uvicorn
from pc_utils import init_pinecone, delete_namespace, namespace_exists
from utils import process_pdf, ask_question

app = FastAPI()

# Initialize Pinecone
PINECONE_API_KEY = os.environ.get("PINECONE_API_KEY")
PINECONE_API_ENV = os.environ.get("PINECONE_API_ENV")
INDEX_NAME = os.environ.get("INDEX_NAME")
pinecone_index = init_pinecone(PINECONE_API_KEY, INDEX_NAME)

@app.post("/upload/")
async def upload_pdf(request: Request):
    request_json = await request.json()
    session_id = str(request_json["session_id"])
    namespace = f"user_{session_id}"  # Unique namespace for each user
    file_path = request_json["file_path"]
    
    if namespace_exists(pinecone_index, namespace):
        delete_namespace(pinecone_index, namespace)
    
    process_pdf(file_path, namespace, pinecone_index)
    
    return {"session_id": session_id, "namespace": namespace}

@app.post("/query/")
async def query_pdf(session_id: str = Form(...), query: str = Form(...)):
    namespace = f"user_{session_id}"
    
    if not namespace_exists(pinecone_index, namespace):
        return JSONResponse(content={"response": "No PDF uploaded for this session."})
    
    response = ask_question(query, session_id, pinecone_index)
    return JSONResponse(content={"response": response})

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)