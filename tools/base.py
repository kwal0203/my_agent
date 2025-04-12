from functools import wraps
from typing import Callable, Dict, Type

from pydantic import BaseModel

tool_registry = []


class Tool:
    def __init__(
        self, name: str, func: Callable, description: str, input_model: type[BaseModel]
    ) -> None:
        self.name = name
        self.func = func
        self.description = description
        self.input_model = input_model

    def run(self, input_data: Dict) -> str:
        print(
            f"Running tool {self.name} with input {input_data}, type: {type(input_data)}"
        )
        validated = self.input_model(**input_data)
        print(f"Validated input: {validated}, type: {type(validated)}")
        return self.func(validated)

    def get_schema(self) -> Dict:
        return {
            "type": "function",
            "name": self.name,
            "description": self.description,
            "parameters": self.input_model.model_json_schema(),
        }

    def __str__(self):
        return f"{self.name}: {self.description}"


def tool(name: str, description: str, input_model: Type[BaseModel]):
    def decorator(func: Callable):
        t = Tool(name=name, func=func, description=description, input_model=input_model)
        tool_registry.append(t)

        @wraps(func)
        def wrapper(input_data):
            return t.run(input_data)

        wrapper._tool = t
        return wrapper

    return decorator


def print_registry():
    print("Tool Registry:")
    for t in tool_registry:
        print(f"Name: {t.name}")
        print(f"Description: {t.description}")
        print(f"Input Model: {t.input_model}")
        print(f"Schema: {t.get_schema()}")
