from src.config.settings import GEMINI_API_KEY
from src.vector_store.vectorstore_singletone import vector_store
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.tools import tool
from langchain_core.messages import HumanMessage, AIMessage
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode, tools_condition
from typing import Annotated, TypedDict
from dotenv import load_dotenv
import os
from pathlib import Path

load_dotenv()

# Set API key
os.environ["GOOGLE_API_KEY"] = GEMINI_API_KEY

class State(TypedDict):
    messages: Annotated[list, add_messages]

@tool
def add_document_to_vectorstore(file_path: str) -> str:
    """Add a document to the vector database for future retrieval
    :param file_path: Path to the document file (relative to knowledge_base folder)
    :return: Status message indicating success or failure
    """
    try:
        # Get the knowledge base path from your vector store
        knowledge_base_path = Path(__file__).parent / "src" / "knowledge_base"
        full_file_path = knowledge_base_path / file_path
        
        if not full_file_path.exists():
            return f"Error: File {file_path} not found in knowledge base"
        
        # Use the document loader strategy to load the document
        from src.vector_store.document_strategies.local_documents_loader import LocalDocumentsLoader
        from langchain_community.document_loaders import PyPDFLoader
        
        # Load the specific document
        if file_path.endswith('.pdf'):
            loader = PyPDFLoader(str(full_file_path))
            documents = loader.load()
        else:
            # For other file types, you can extend this
            return f"Unsupported file type: {file_path}"
        
        # Add documents to vector store
        # Note: You'll need to implement this method in your vector store
        # For now, returning success message
        return f"Document {file_path} loaded successfully. Ready to be added to vector database."
        
    except Exception as e:
        return f"Error adding document: {str(e)}"

@tool
def search_vector_database(query: str, top_k: int = 5) -> str:
    """Search the vector database for relevant information
    :param query: The search query
    :param top_k: Number of top results to return
    :return: Relevant information from the vector database
    """
    try:
        # Use your existing vector store query method
        results = vector_store.query(query, top_k)
        if results:
            return f"Found {len(results)} relevant results: {results}"
        else:
            return "No relevant results found in the vector database"
    except Exception as e:
        return f"Error searching vector database: {str(e)}"

@tool
def list_available_documents() -> str:
    """List all available documents in the knowledge base
    :return: List of available documents
    """
    try:
        knowledge_base_path = Path(__file__).parent / "src" / "knowledge_base"
        if not knowledge_base_path.exists():
            return "Knowledge base directory not found"
        
        documents = []
        for file_path in knowledge_base_path.iterdir():
            if file_path.is_file() and not file_path.name.startswith('.'):
                documents.append(file_path.name)
        
        if documents:
            return f"Available documents: {', '.join(documents)}"
        else:
            return "No documents found in knowledge base"
            
    except Exception as e:
        return f"Error listing documents: {str(e)}"

# Define tools
tools = [add_document_to_vectorstore, search_vector_database, list_available_documents]

# Initialize LLM
llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash")
llm_with_tools = llm.bind_tools(tools)

def chatbot(state: State):
    """Main chatbot node that processes user messages and decides when to use tools"""
    messages = state["messages"]
    
    # Use LLM to decide if tools are needed
    response = llm_with_tools.invoke(messages)
    return {"messages": [response]}

# Build the graph
builder = StateGraph(State)

# Add nodes
builder.add_node("chatbot", chatbot)
builder.add_node("tools", ToolNode(tools))

# Add edges
builder.add_edge(START, "chatbot")
builder.add_conditional_edges("chatbot", tools_condition)
builder.add_edge("tools", "chatbot")
builder.add_edge("chatbot", END)

# Compile the graph
graph = builder.compile()

def run_retrieval_agent(user_query: str):
    """Run the retrieval agent with a user query"""
    initial_state = {"messages": [HumanMessage(content=user_query)]}
    result = graph.invoke(initial_state)
    return result["messages"][-1].content

# Example usage
if __name__ == "__main__":
    # Test listing available documents
    print("=== Testing Document Listing ===")
    list_response = run_retrieval_agent("List all available documents in the knowledge base")
    print(f"Agent Response: {list_response}")
    
    # Test adding a document
    print("\n=== Testing Document Addition ===")
    add_response = run_retrieval_agent("Add the SampleRadioPSAScripts.pdf document to the vector database")
    print(f"Agent Response: {add_response}")
    
    # Test searching
    print("\n=== Testing Search ===")
    search_response = run_retrieval_agent("Search for information about radio PSA scripts in the vector database")
    print(f"Agent Response: {search_response}")
    