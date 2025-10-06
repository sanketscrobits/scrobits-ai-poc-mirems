from typing import Literal
from langgraph.graph import StateGraph, START, END
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import ChatPromptTemplate
from src.agents.state import QueryAgentState
from src.tools.query_tool import get_context
from src.utils.yaml_loader import load_prompts
from src.agents.retriver_agent import create_query_agent
from settings import GOOGLE_API_KEY
prompts = load_prompts("src/utils/prompts.yml")


def retriever_agent(state: QueryAgentState) -> QueryAgentState:
    """Retrieve relevant documents for the user query using existing retriever agent"""
    try:
        agent = create_query_agent(api_key=GOOGLE_API_KEY)
        result = agent.invoke({"input": state["user_query"]})
        
        retrieved_docs = result.get("output", "")
        state["retrieved_documents"] = [retrieved_docs] if isinstance(retrieved_docs, str) else retrieved_docs
        state["metadata"] = {"retrieval_status": "success", "retrieval_method": "existing_agent"}
        state["retry_count"] = state.get("retry_count", 0)
        
    except Exception as e:
        state["retrieved_documents"] = []
        state["metadata"] = {"retrieval_status": "failed", "error": str(e)}
        state["retry_count"] = state.get("retry_count", 0)
    return state

def reranker_agent(state: QueryAgentState) -> QueryAgentState:
    """Rerank and filter retrieved documents by true semantic relevance"""
    model = ChatGoogleGenerativeAI(model="gemini-2.0-flash", temperature=0.1)
    
    model_prompt = ChatPromptTemplate([
        ("system", prompts.get("reranker_agent_prompt")),
        ("user", "User Query: {query}\n\nRetrieved Document Chunks:\n{documents}\n\nRerank these chunks by semantic relevance:")
    ])
    
    chain = model_prompt | model
    response = chain.invoke({
        "query": state["user_query"],
        "documents": "\n---\n".join(state["retrieved_documents"])
    })
    
    reranked_text = response.content
    state["reranked_documents"] = [reranked_text] if reranked_text else state["retrieved_documents"]
    
    return state

def analyst_generator_agent(state: QueryAgentState) -> QueryAgentState:
    """Core reasoning agent - generates comprehensive, citation-backed response"""
    model = ChatGoogleGenerativeAI(model="gemini-2.0-flash", temperature=0.3)
    
    model_prompt = ChatPromptTemplate([
        ("system", prompts.get("analyst_agent_prompt")),
        ("user", "User Query: {query}\n\nTop-Ranked Context Chunks:\n{context}\n\nGenerate a comprehensive, citation-backed response:")
    ])
    
    chain = model_prompt | model
    response = chain.invoke({
        "query": state["user_query"],
        "context": "\n---\n".join(state["reranked_documents"])
    })
    
    state["analysis_result"] = response.content
    return state

def evaluator_agent(state: QueryAgentState) -> QueryAgentState:
    model = ChatGoogleGenerativeAI(model = "gemini-2.0-flash", temperature=0.3)

    model_prompt = ChatPromptTemplate([
        ("system", prompts.get("evaluator_agent_prompt")),
        ("user", "User Query: {query}\n\nTop-Ranked Context Chunks:\n{context}\n\nGenerate a comprehensive, citation-backed response:")
    ])

    

def presenter_agent(state: QueryAgentState) -> QueryAgentState:
    """Presenter Agent - displays the final result in console"""
    print("\n=== QUERY RESULT ===")
    print("Query:", state.get("user_query"))
    print("\nFinal Answer:\n", state.get("analysis_result", ""))
    print("\nEvaluation score:", state.get("evaluation_score"))
    print("Evaluation feedback:", state.get("evaluation_feedback"))
    return state

def should_regenerate(state: QueryAgentState) -> Literal["retriever_agent", "presenter_agent"]:
    """Decide whether to route back to Retriever Agent based on quality issues"""
    if state.get("evaluation_score", 0) < 6.0 and state.get("retry_count", 0) < 2:
        state["retry_count"] = state.get("retry_count", 0) + 1
        return "retriever_agent"
    return "presenter_agent"

# Create the workflow graph
def create_query_workflow():
    graph = StateGraph(QueryAgentState)
    
    # nodes for each agent
    graph.add_node("retriever_agent", retriever_agent)
    graph.add_node("reranker_agent", reranker_agent)
    graph.add_node("analyst_generator_agent", analyst_generator_agent)
    graph.add_node("evaluator_agent", evaluator_agent)
    graph.add_node("presenter_agent", presenter_agent)
    
    # flow with feedback loop
    graph.add_edge(START, "retriever_agent")
    graph.add_edge("retriever_agent", "reranker_agent")
    graph.add_edge("reranker_agent", "analyst_generator_agent")
    graph.add_edge("analyst_generator_agent", "evaluator_agent")
    
    # Critical decision point: route back to retriever if quality issues found
    graph.add_conditional_edges("evaluator_agent", should_regenerate)
    graph.add_edge("presenter_agent", END)
    
    return graph.compile()

# Usage
if __name__ == "__main__":
    workflow = create_query_workflow()
    
    # Optional: Generate workflow diagram
    try:
        workflow.get_graph().draw_png(output_file_path="query_agent_workflow.png")
    except:
        pass
    
    # Test the workflow
    result = workflow.invoke({
        "user_query": "What initiative did the federal government announce regarding AI?",
        "retrieved_documents": [],
        "reranked_documents": [],
        "analysis_result": "",
        "evaluation_score": 0.0,
        "evaluation_feedback": "",
        "final_response": "",
        "metadata": {},
        "retry_count": 0,
        "has_hallucinations": False,
        "citations_complete": True
    })
    
    print(f"Final Evaluation Score: {result.get('evaluation_score', 'N/A')}/10")
    print(f"Total Retry Attempts: {result.get('retry_count', 0)}")