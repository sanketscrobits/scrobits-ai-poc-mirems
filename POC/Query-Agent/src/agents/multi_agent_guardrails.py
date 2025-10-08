from langgraph.graph import StateGraph, START, END
from langchain_google_genai import ChatGoogleGenerativeAI
from typing import TypedDict, Literal
from src.agents.retriver_agent import create_query_agent
from settings import GOOGLE_API_KEY 
from guardrails import Guard
from guardrails.hub import  ProfanityFree
from guardrails.errors import ValidationError

model = ChatGoogleGenerativeAI(model="gemini-2.5-flash",google_api_key = GOOGLE_API_KEY)
query_agent = create_query_agent(api_key= GOOGLE_API_KEY)
guard = Guard().use(
    ProfanityFree, on_fail="exception"
)

class ResponseSchema(TypedDict):
    user_query: str
    query_response: str
    evaluation_state: Literal["True", "False"]
    retry_count: int
    instruction: str


def retriver_agent(state: ResponseSchema) -> ResponseSchema:
    user_query = state["user_query"]
    instruction = state["instruction"]
    modified_input = {"input": f"{user_query}\n\n{instruction}" if instruction else user_query}
    result = query_agent.invoke({"input": modified_input})
    response_str = result["output"]

    return {
        "user_query": user_query,
        "query_response": response_str,
        "evaluation_state": "",
        "retry_count": state["retry_count"] + 1,
        "instruction": instruction
    }

def evaluator_agent(state: ResponseSchema) -> ResponseSchema:
    user_query = state["user_query"]
    query_response = state["query_response"]
    llm_text = query_response
    if state["retry_count"] > 3:
        return {
            "user_query": user_query,
            "query_response": "Max retries exceeded. Response could not be generated without profanity.",
            "evaluation_state": "True",
            "instruction": "" 
        }

    try:
        validated_output = guard.validate(llm_text)
        return {
            "user_query": user_query,
            "query_response": str(validated_output), 
            "evaluation_state": "True",
            "instruction": ""
        }
    except ValidationError:
        retry_instruction = "Rephrase the response to be completely profanity-free. Avoid any explicit language, slurs, or direct quotes of offensive content. Summarize factually and neutrally."
        return {
            "user_query": user_query,
            "query_response": llm_text,  
            "evaluation_state": "False",
            "instruction": retry_instruction
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

if __name__ == "__main__":
    initial_state = {
        "user_query": "What did the anonymous BCGEU member post on social media about the government's raise offer during the strike?",
        "query_response": "",
        "evaluation_state": "",
        "retry_count": 0,
        "instruction": ""
    }

    final_state = workflow.invoke(initial_state, config={"verbose": True})

    print(final_state)
