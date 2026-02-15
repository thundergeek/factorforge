from openai import OpenAI
import random


class OllamaClient:
    def __init__(self):
        # Multiple Ollama endpoints for load balancing
        self.endpoints = [
            {"url": "http://localhost:11434/v1", "name": "GPU0 (1070Ti)"},
            {"url": "http://localhost:11435/v1", "name": "GPU1 (1060)"},
        ]
        self.current_idx = 0
        
        # Test which endpoints are available
        self.available_endpoints = []
        for ep in self.endpoints:
            try:
                client = OpenAI(base_url=ep["url"], api_key="ollama", timeout=5)
                # Test connection
                client.models.list()
                self.available_endpoints.append(ep)
                print(f"✅ Connected to Ollama on {ep['name']}")
            except Exception as e:
                print(f"⚠️  Ollama on {ep['name']} not available: {e}")
        
        if not self.available_endpoints:
            raise RuntimeError("No Ollama endpoints available!")
        
        print(f"🚀 Using {len(self.available_endpoints)} GPU(s) for LLM inference")
    
    def _get_next_endpoint(self):
        """Round-robin between available endpoints"""
        ep = self.available_endpoints[self.current_idx]
        self.current_idx = (self.current_idx + 1) % len(self.available_endpoints)
        return ep
    
    def chat(self, messages: list, model: str = "llama3.1:latest", temperature: float = 0.8):
        endpoint = self._get_next_endpoint()
        
        client = OpenAI(
            base_url=endpoint["url"],
            api_key="ollama",
            timeout=120
        )
        
        try:
            resp = client.chat.completions.create(
                model=model,
                messages=messages,
                temperature=temperature,
                max_tokens=512,
            )
            return resp.choices[0].message.content
        except Exception as e:
            print(f"⚠️  LLM call failed on {endpoint['name']}: {e}")
            # Try fallback to other GPU
            if len(self.available_endpoints) > 1:
                fallback = self.available_endpoints[0] if self.current_idx > 0 else self.available_endpoints[1]
                client = OpenAI(base_url=fallback["url"], api_key="ollama", timeout=120)
                resp = client.chat.completions.create(
                    model=model, messages=messages, temperature=temperature, max_tokens=512
                )
                return resp.choices[0].message.content
            else:
                raise


ollama_client = OllamaClient()
