from pathlib import Path
from pydantic_settings import BaseSettings
from pydantic import Field


class Settings(BaseSettings):
    data_dir: Path = Field(default=Path("data"))
    results_dir: Path = Field(default=Path("data/results"))
    start_date: str = Field(default="2018-01-01")
    end_date: str = Field(default="2025-12-31")
    universe_symbols: str = Field(default="AAPL,MSFT,GOOGL,AMZN,NVDA,TSLA,META")
    llm_provider: str = Field(default="ollama")
    ollama_base_url: str = Field(default="http://localhost:11434/v1")
    ollama_api_key: str = Field(default="ollama")
    ollama_model: str = Field(default="llama3.1:latest")
    max_generations: int = Field(default=3)
    agents_per_generation: int = Field(default=3)
    top_k_factors: int = Field(default=5)

    class Config:
        env_prefix = ""


settings = Settings()
settings.data_dir.mkdir(parents=True, exist_ok=True)
settings.results_dir.mkdir(parents=True, exist_ok=True)
