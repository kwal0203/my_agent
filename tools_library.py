from pydantic import BaseModel
from tools import Tool


class CalculatorInput(BaseModel):
    expression: str


class SearchInput(BaseModel):
    query: str


def calculator_tool(input: CalculatorInput):
    try:
        return str(eval(input.expression))
    except:
        return "Error evaluating."


calculator = Tool(
    name="calculator",
    func=calculator_tool,
    description="Evaluates basic math expressions.",
    input_model=CalculatorInput,
)


def search_web_func(input: SearchInput):
    return f"Fake search result for '{input.query}'"


search_web = Tool(
    name="search_web",
    func=search_web_func,
    description="Searches the web for information",
    input_model=SearchInput,
)
