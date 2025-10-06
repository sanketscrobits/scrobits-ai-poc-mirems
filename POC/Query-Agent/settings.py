from dotenv import load_dotenv
from os import getenv
from pathlib import Path

load_dotenv(".env")

BASE_DIR = Path(__file__).resolve().parent.parent

GOOGLE_API_KEY=getenv("GEMINI_API_KEY")
PINECONE_API_KEY=getenv("PINECONE_API_KEY")
PINECONE_INDEX_NAME=getenv("PINECONE_INDEX_NAME")
PINECONE_REGION=getenv("PINECONE_REGION")
PINECONE_HOST=getenv("PINECONE_HOST")
WHATSAPP_TOKEN=getenv("WA_ACCESS_TOKEN")
PHONE_NUMBER_ID=getenv("WA_PHONE_NUMBER_ID")
GUARDRAILS_API_KEY=getenv("GUARDRAILS_API_KEY")