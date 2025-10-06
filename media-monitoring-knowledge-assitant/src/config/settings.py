from dotenv import load_dotenv
from os import getenv
from pathlib import Path

load_dotenv(".env")

BASE_DIR = Path(__file__).resolve().parent.parent

ASTRA_DB_APPLICATION_TOKEN=getenv("ASTRA_DB_APPLICATION_TOKEN")
ASTRA_DB_API_ENDPOINT=getenv("ASTRA_DB_API_ENDPOINT")
ASTRA_DB_COLLECTION_NAME=getenv("ASTRA_DB_COLLECTION_NAME")
EMBEDDING_DIMENSION=getenv("EMBEDDING_DIMENSION", '768')
ASTRA_DB_ID=getenv("ASTRA_DB_ID")
GEMINI_API_KEY=getenv("GEMINI_API_KEY")