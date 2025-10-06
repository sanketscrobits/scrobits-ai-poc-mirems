import sys
import os
from langchain_google_genai import ChatGoogleGenerativeAI
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
from agents.retriver_agent import query_agent
from settings import GOOGLE_API_KEY

query = input("Enter your question: ")

# Use the ReAct agent directly (this was working)
result = query_agent.invoke({"input": query})

print("Question:", query)
print("="*50)
print("Answer:", result["output"])