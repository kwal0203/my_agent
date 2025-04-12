import os

from dotenv import load_dotenv

import tools.calculator
from agent import Agent
from llm import LLM
from tools.base import tool_registry

# Load environment variables from .env file
load_dotenv()

# Get API key from environment
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    print("Error: OPENAI_API_KEY environment variable is not set")
    print("Please set it using: export OPENAI_API_KEY='your-api-key'")
    exit(1)

print("-------------------")
for tool in tool_registry:
    print(tool.get_schema())
print("-------------------")

llm = LLM(api_key=api_key)
agent = Agent(llm)

# Run it
# agent.run("What is the square root of 98765?")
# agent.run("What is the square root of 56789?")
# agent.run("What is the square root of 23 * 23?")
# agent.run("What is the square root of (1 + 2 + 3 + 4 + 5 + 6)?")
agent.run("What is the square root of -89?")
