from memory import Memory
from tools_library import CalculatorInput, SearchInput


class Agent:
    def __init__(self, llm, tools):
        self.llm = llm
        self.tools = {tool.name: tool for tool in tools}
        self.memory = Memory()
        self.system_prompt = self._generate_system_prompt()

    def _generate_system_prompt(self):
        tools_description = "\n".join(
            [f"{name}: {tool.description}" for name, tool in self.tools.items()]
        )
        return f"""You are a helpful AI agent. You can use tools to help with user queries.

Available tools:
{tools_description}

Respond in the following format:
Thought: ...
Action: <tool_name>
Action Input: <input>

If you are done:
Final Answer: <your answer>
"""

    def run(self, user_input):
        self.memory = Memory()
        self.memory.add("system", self.system_prompt)
        self.memory.add("user", user_input)

        while True:
            response = self.llm.chat(self.memory.get())
            print("Agent:\n", response)
            self.memory.add("assistant", response)

            if "Final Answer:" in response:
                break

            if "Action:" in response:
                lines = response.splitlines()
                action_line = [l for l in lines if l.startswith("Action:")][0]
                input_line = [l for l in lines if l.startswith("Action Input:")][0]

                tool_name = action_line.split("Action:")[1].strip()
                tool_input = input_line.split("Action Input:")[1].strip()

                if tool_name in self.tools:
                    tool = self.tools[tool_name]
                    if tool_name == "calculator":
                        tool_input = CalculatorInput(expression=tool_input)
                    if tool_name == "search_web":
                        tool_input = SearchInput(query=tool_input)
                    result = tool.run(tool_input)
                    self.memory.add(
                        "function", f"{tool_name} returned: {result}", name=tool_name
                    )
                else:
                    self.memory.add(
                        "function", f"Error: unknown tool '{tool_name}'", name="error"
                    )
