import os
from openai import OpenAI

class OllamaClient:
    def __init__(self):
        self.base_url = os.getenv("OLLAMA_BASE_URL", "http://ollama:11434")
        self.model = os.getenv("OLLAMA_MODEL", "llama3.2:3b")
        
        self.client = OpenAI(
            base_url=f"{self.base_url}/v1",
            api_key="ollama"
        )
        
        print(f"✅ Connected to Ollama at {self.base_url}")

    def chat(self, messages, temperature=0.7, max_tokens=2000):
        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens
        )
        return response.choices[0].message.content

ollama_client = OllamaClient()
