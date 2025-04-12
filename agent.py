import json

from memory import Memory
from prompts import SYS_PROMPT
from tools.base import tool_registry


def debug_fn(action_line, input_line, tool_name, tool_input, tools):
    print("--------------------------------")
    print(f"action line: {action_line}")
    print(f"input line:  {input_line}")
    print(f"tool name:   {tool_name}")
    print(f"tool input:  {tool_input}")
    print(f"tools:       {tools}")
    print("--------------------------------")


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

    def run(self, user_input, debug=True):
        self.memory = Memory()
        self.memory.add("system", self.system_prompt)
        self.memory.add("user", user_input)
        print(self.memory.get()[-1]["content"])
        while True:
            response = self.llm.fn_calling(self.memory.get(), self.tools_schema)
            # print("Agent:\n", response)
            self.memory.add("assistant", response)

            if response.type == "function_call":
                tool_name = response.name
                tool_arguments = json.loads(response.arguments)
                print(f"Calling tool: {tool_name} with arguments: {tool_arguments}")
                if tool_name == "calculator":
                    result = self.tools["calculator"].run(tool_arguments)
                else:
                    result = "Unknown tool"
            else:
                result = response.content

            print(result[0].text)
            break
            # if "Final Answer:" in response:
            #     break

            # if "Action:" in response:
            #     lines = response.splitlines()
            #     action_line = [l for l in lines if l.startswith("Action:")][0]
            #     input_line = [l for l in lines if l.startswith("Action Input:")][0]

            #     tool_name = action_line.split("Action:")[1].strip()
            #     tool_input = input_line.split("Action Input:")[1].strip()

            #     if debug:
            #         debug_fn(action_line, input_line, tool_name, tool_input, self.tools)

            #     if tool_name in self.tools:
            #         tool = self.tools[tool_name]
            #         if tool_name == "calculator":
            #             tool_input = {"expression": tool_input}

            #         result = tool.run(tool_input)
            #         self.memory.add(
            #             "function", f"{tool_name} returned: {result}", name=tool_name
            #         )
            #     else:
            #         self.memory.add(
            #             "function", f"Error: unknown tool '{tool_name}'", name="error"
            #         )
