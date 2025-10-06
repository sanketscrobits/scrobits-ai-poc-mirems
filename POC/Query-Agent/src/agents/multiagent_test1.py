from langgraph.graph import StateGraph, START, END
from langchain_google_genai import ChatGoogleGenerativeAI
from typing import TypedDict, Literal
from src.agents.retriver_agent import create_query_agent
from settings import GOOGLE_API_KEY, GUARDRAILS_API_KEY


model = ChatGoogleGenerativeAI(model="gemini-2.5-flash", google_api_key=GOOGLE_API_KEY)
query_agent = create_query_agent(GOOGLE_API_KEY)

class ResponseSchema(TypedDict):
    user_query: str
    query_response: str
    evaluation_state: Literal["pass", "fail"]

def retriver_agent(state: ResponseSchema) -> ResponseSchema:
    user_query = state["user_query"]
    result = query_agent.invoke({"input": user_query})

    return {"query_response" :result}

graph = StateGraph(ResponseSchema)

graph.add_node('retriver_agent', retriver_agent)

graph.add_edge(START, 'retriver_agent')
graph.add_edge('retriver_agent', END)

workflow = graph.compile()

initial_state = {'user_query':'What trend did Statistics Canada report about electric vehicle sales in Q2 2025?'}

final_state = workflow.invoke(initial_state, config={"verbose": True})

print(final_state)
