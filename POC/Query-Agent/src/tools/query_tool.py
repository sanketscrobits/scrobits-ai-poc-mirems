from sentence_transformers import SentenceTransformer
from pinecone import Pinecone
from settings import PINECONE_API_KEY, PINECONE_INDEX_NAME
from langchain.tools import tool

@tool
def get_context(user_question: str) -> str:
    """
    This function helps to answer user question by retrieving relevant context from documents.
    
    Args: 
        user_question: User question in string format
        
    Returns: 
        Context related to user's question in string format
    """
    try:
        model = SentenceTransformer("all-MiniLM-L6-v2")
        pc = Pinecone(api_key=PINECONE_API_KEY)
        query_embedding = model.encode(user_question, convert_to_numpy=True)
        index = pc.Index(PINECONE_INDEX_NAME)

        results = index.query(
            vector=query_embedding.tolist(),
            top_k=20,
            include_metadata=True,
            score_threshold=0.7
        )
        
        if results["matches"]:
            context = results["matches"][0]["metadata"]["chunk_text"]
            return context
        else:
            return "No relevant context found for the question."
            
    except Exception as e:
        return f"Error retrieving context: {str(e)}"

if __name__ == "__main__":
    print(get_context("What initiative did the federal government announce regarding AI?"))