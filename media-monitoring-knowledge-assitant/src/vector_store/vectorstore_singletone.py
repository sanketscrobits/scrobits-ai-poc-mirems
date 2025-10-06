from core.base.singletone import SingletonBase
from document_strategies.base import DocumentLoaderStrategy
from vector_index_strategies.base import VectorIndexStrategy
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from document_strategies.local_documents_loader import LocalDocumentsLoader
from config.settings import BASE_DIR
from vector_index_strategies.astradb_vector_index import AstraDBVectorIndex
from config.settings import ASTRA_DB_APPLICATION_TOKEN, ASTRA_DB_API_ENDPOINT, ASTRA_DB_COLLECTION_NAME


class VectorstoreSingletone(SingletonBase):

    def __init__(
        self, embeddings_model,
        document_loader_strategy:DocumentLoaderStrategy, 
        vector_store:VectorIndexStrategy
        ):
       self._embeddings_model = embeddings_model
       self._vector_store = vector_store
       
    def _build_vector_store():
        pass
    def query(self, text:str, topk:int):
       return self._vector_store.query(text,topk) 

vector_store = VectorstoreSingletone(
    embeddings_model=GoogleGenerativeAIEmbeddings("models/gemini-embedding-001"),
    document_loader_strategy=LocalDocumentsLoader(folder_path=f"{BASE_DIR}/knowledge_base"),
    vector_store=AstraDBVectorIndex(
        ASTRA_DB_APPLICATION_TOKEN,
        ASTRA_DB_API_ENDPOINT,
        ASTRA_DB_COLLECTION_NAME,
        GoogleGenerativeAIEmbeddings("models/gemini-embedding-001")
    )
)