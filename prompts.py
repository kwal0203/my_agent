SYS_PROMPT ="""You are a helpful AI agent. You can use tools to help with user queries.

Available tools:
{tools_description}

Respond in the following format:
Thought: ...
Action: <tool_name>
Action Input: <input>

If you are done:
Final Answer: <your answer>
"""