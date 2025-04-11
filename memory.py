# memory.py
class Memory:
    def __init__(self):
        self.messages = []

    def add(self, role, content, name=None):
        message = {"role": role, "content": content}
        if role == "function":
            if name is None:
                raise ValueError("Function messages must have a name")
            message["name"] = name
        self.messages.append(message)

    def get(self):
        return self.messages
