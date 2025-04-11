from pydantic import BaseModel


class Tool:
    def __init__(self, name, func, description, input_model: type[BaseModel]):
        self.name = name
        self.func = func
        self.description = description
        self.input_model = input_model

    def run(self, input_data):
        if isinstance(input_data, BaseModel):
            validated = input_data
        else:
            validated = self.input_model(**input_data)
        return self.func(validated)

    def describe(self):
        fields = self.input_model.model_json_schema()["properties"]
        field_descriptions = {k: v["type"] for k, v in fields.items()}
        return f"{self.name}: {self.description}. Inputs: {field_descriptions}"
