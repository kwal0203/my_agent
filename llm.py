from openai import OpenAI
import os


class LLM:
    def __init__(self, api_key, model="gpt-4"):
        if not api_key:
            print("Warning: No API key provided. Checking environment variable...")
            api_key = os.getenv("OPENAI_API_KEY")
            if not api_key:
                raise ValueError(
                    "API key must be provided either directly or via OPENAI_API_KEY environment variable"
                )

        # Debug: Print first few characters of API key to verify it's being set
        print(f"Using API key starting with: {api_key[:5]}...")

        self.client = OpenAI(api_key=api_key)
        self.model = model

    def chat(self, messages):
        response = self.client.chat.completions.create(
            model=self.model, messages=messages, temperature=0.7
        )
        return response.choices[0].message.content
