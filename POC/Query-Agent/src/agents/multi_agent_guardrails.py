from langgraph.graph import StateGraph, START, END
from langchain_google_genai import ChatGoogleGenerativeAI
from typing import TypedDict, Annotated, Literal
from src.agents.retriver_agent import create_query_agent
from settings import GOOGLE_API_KEY, GUARDRAILS_API_KEY
from guardrails import Guard
from guardrails.hub import QARelevanceLLMEval

model = ChatGoogleGenerativeAI(model="gemini-2.5-flash")
query_agent = create_query_agent(GOOGLE_API_KEY)
guard = Guard().use(
    QARelevanceLLMEval,
    llm_callable="gemini/gemini-2.5-flash",
    on_fail="exception",
)

class ResponseSchema(TypedDict):
    user_query: str
    query_response: str
    evaluation_state: Literal["pass", "fail"]


def retriver_agent(state: ResponseSchema) -> ResponseSchema:
    user_query = state["user_query"]
    result = query_agent.invoke({"input": user_query})

    return {"query_response" :result}

def evaluator_agent(state: ResponseSchema) -> ResponseSchema:
    user_query = state["user_query"]
    query_response = state["query_response"]
    validated_output = guard.validate(
        llm_response = query_response,
        metadata={
            "original_prompt": user_query,
        },
    )
    print(validated_output)

graph = StateGraph(ResponseSchema)

graph.add_node('retriver_agent', retriver_agent)
graph.add_node('evaluator_agent', evaluator_agent)

graph.add_edge(START, 'retriver_agent')
graph.add_edge('retriver_agent', 'evaluator_agent')
graph.add_edge('evaluator_agent', END)

workflow = graph.compile()

initial_state = {'user_query':'What trend did Statistics Canada report about electric vehicle sales in Q2 2025?'}

final_state = workflow.invoke(initial_state, config={"verbose": True})

print(final_state)
