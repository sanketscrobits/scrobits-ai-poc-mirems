from fastapi import FastAPI
from pydantic import BaseModel


from src.vector_store.vector_index_strategies.astradb_vector_index import AstraDBVectorIndex

app = FastAPI()

class ChatRequest(BaseModel):
    query: str

@app.get("/")
def root():
    return{"message": "Hello world"}

vector_store = AstraDBVectorIndex(
        ASTRA_DB_APPLICATION_TOKEN="<ASTRA_DB_APPLICATION_TOKEN>",
        ASTRA_DB_API_ENDPOINT="<ASTRA_DB_API_ENDPOINT>",
        ASTRA_DB_COLLECTION_NAME="<ASTRA_DB_COLLECTION_NAME>",
        ASTRA_DB_ID="<ASTRA_DB_ID>",
        GEMINI_API_KEY="<GEMINI_API_KEY>"
)

@app.post("/")
def assistant_api(request: ChatRequest):
    result = vector_store.query(request.query, 32)
    return {"message":f"{result}!"}