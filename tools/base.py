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
        validated = self.input_model(**input_data)
        return self.func(validated)

    def get_schema(self) -> Dict:
        return {
            "name": self.name,
            "description": self.description,
            "parameters": self.input_model.model_json_schema(),
        }


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
