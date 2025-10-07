from langgraph.graph import StateGraph, START, END
from langchain_google_genai import ChatGoogleGenerativeAI
from typing import TypedDict, Literal
from src.agents.retriver_agent import create_query_agent
from settings import GOOGLE_API_KEY 
from guardrails import Guard
from guardrails.hub import  ProfanityFree

model = ChatGoogleGenerativeAI(model="gemini-2.5-flash",google_api_key = GOOGLE_API_KEY)
query_agent = create_query_agent(api_key= GOOGLE_API_KEY)
guard = Guard().use(
    ProfanityFree, on_fail="exception"
)

class ResponseSchema(TypedDict):
    user_query: str
    query_response: str
    evaluation_state: Literal["True", "False"]


def retriver_agent(state: ResponseSchema) -> ResponseSchema:
    user_query = state["user_query"]
    result = query_agent.invoke({"input": user_query})

    return {
        "user_query": user_query,
        "query_response": result,
        "evaluation_state": ""
    }

def evaluator_agent(state: ResponseSchema) -> ResponseSchema:
    user_query = state["user_query"]
    query_response = state["query_response"]
    llm_text = query_response["output"]
    validated_output = guard.validate( llm_text )

    return {
        "user_query": user_query,
        "query_response": llm_text,
        "evaluation_state": validated_output.validation_passed
    }

def evaluation_edge(state: ResponseSchema):
    return "retriver_agent" if state["evaluation_state"] == "False" else END

graph = StateGraph(ResponseSchema)

graph.add_node('retriver_agent', retriver_agent)
graph.add_node('evaluator_agent', evaluator_agent)

graph.add_edge(START, 'retriver_agent')
graph.add_edge('retriver_agent', 'evaluator_agent')
graph.add_conditional_edges(
    "evaluator_agent",
    evaluation_edge,
    {
        "retriver_agent": "retriver_agent",
        END: END
    }
)

workflow = graph.compile()

# initial_state = {
#     "user_query": "What trend did Statistics Canada report about electric vehicle sales in Q2 2025?",
#     "query_response": "",
#     "evaluation_state": ""
# }

# final_state = workflow.invoke(initial_state, config={"verbose": True})

# print(final_state)
