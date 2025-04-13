import json

from memory import Memory
from prompts import SYS_PROMPT
from tools.base import tool_registry


class Agent:
    def __init__(self, llm):
        self.llm = llm
        self.tools = {i.name: i for i in tool_registry}
        self.tools_schema = [tool.get_schema() for tool in self.tools.values()]
        self.memory = Memory()
        self.system_prompt = self._generate_system_prompt()

    def _generate_system_prompt(self):
        tools_description = "\n".join(
            [f"{name}: {tool.description}" for name, tool in self.tools.items()]
        )
        return SYS_PROMPT.format(tools_description=tools_description)

    def find_tool_by_name(self, name: str):
        if name in self.tools:
            return self.tools[name]
        raise ValueError(f"No tool found with name: {name}")

    def run(self, user_input: str, max_turns: int = 10, debug: bool = True):
        self.memory = Memory()
        self.memory.add("system", self.system_prompt)
        self.memory.add("user", user_input)
        print(self.memory.get()[-1]["content"])

        for turn in range(max_turns):
            print(f"\n🧠 Turn {turn + 1}")

            response = self.llm.fn_calling(self.memory.get(), self.tools_schema)
            self.memory.add("assistant", response)

            if response.type == "function_call":
                tool_name = response.name
                tool_arguments = json.loads(response.arguments)

                print(f"🔧 calling {tool_name} tool with arguments: {tool_arguments}")

                tool = self.find_tool_by_name(name=tool_name)
                result = tool.run(tool_arguments)

                self.memory.add(
                    "function", f"{tool_name} returned: {result}", name=tool_name
                )
            elif response.type == "message":
                result = response.content[0].text
                self.memory.add("assistant", result)
                print(f"\n🤖 assistant:\n{result}")
                break
            elif turn == max_turns - 1:
                print("🤖 agent reached max turns. Ending conversation.")
                break
