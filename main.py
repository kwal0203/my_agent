import os

from dotenv import load_dotenv

from agent import Agent
from llm import LLM
from tools_library import calculator, search_web

# Load environment variables from .env file
load_dotenv()

tools = [
    search_web,
    calculator,
]

# Get API key from environment
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    print("Error: OPENAI_API_KEY environment variable is not set")
    print("Please set it using: export OPENAI_API_KEY='your-api-key'")
    exit(1)

llm = LLM(api_key=api_key)
agent = Agent(llm, tools)

# Run it
agent.run("What is the square root of 98765?")
