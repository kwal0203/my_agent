from pydantic import BaseModel
from sympy import SympifyError, cos, exp, ln, log, sin, sqrt, sympify, tan

from tools.base import tool


class CalculatorInput(BaseModel):
    expression: str


@tool(
    name="calculator",
    description="Evaluates a mathematical expression like '2 + 3 * (4 - 1)'.",
    input_model=CalculatorInput,
)
def calculator_tool(input: CalculatorInput):
    try:
        expr = sympify(
            input.expression,
            locals={
                "sqrt": sqrt,
                "sin": sin,
                "cos": cos,
                "tan": tan,
                "exp": exp,
                "log": log,
                "ln": ln,
            },
        )
        result = expr.evalf()
        return str(result)
    except SympifyError:
        return "Error: invalid expression."
    except Exception as e:
        return f"Error: {str(e)}."
