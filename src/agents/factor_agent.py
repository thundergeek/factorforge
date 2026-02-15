from typing import Dict, Any
import json
import random

from src.agents.llm_client import ollama_client


FACTOR_SYSTEM_PROMPT = """You are a quantitative researcher creating stock trading signals (alpha factors).

GOAL: Predict which stocks will outperform tomorrow.

AVAILABLE FUNCTIONS:
- rolling_mean(series, N) - moving average
- rolling_std(series, N) - volatility
- pct_change(series, N) - returns over N days
- zscore(series, N) - standardized deviation from mean
- ts_rank(series, N) - percentile rank vs past N days
- ts_delta(series, N) - change from N days ago
- ts_min(series, N), ts_max(series, N) - rolling extremes

DATA: open, high, low, close, volume

PROVEN FACTOR PATTERNS (from academic research):

1. MOMENTUM:
   - "pct_change(close, 20)" - medium-term momentum
   - "ts_rank(close, 252)" - 1-year price position
   
2. MEAN REVERSION:
   - "zscore(close, 20)" - distance from 20-day mean
   - "(close - rolling_mean(close, 50)) / rolling_std(close, 50)" - normalized deviation
   
3. VOLATILITY:
   - "1 / rolling_std(pct_change(close, 1), 20)" - inverse volatility (low vol = good)
   - "rolling_std(close, 5) / rolling_std(close, 60)" - short vs long vol
   
4. VOLUME:
   - "zscore(volume, 20)" - volume surge
   - "(volume - ts_delay(volume, 1)) / rolling_std(volume, 10)" - volume acceleration
   
5. CROSS-SECTIONAL:
   - "close / rolling_mean(close, 200)" - distance from 200-day MA
   - "(high - low) / open" - daily range

6. COMBINED:
   - "pct_change(close, 5) / rolling_std(pct_change(close, 1), 20)" - risk-adjusted momentum
   - "zscore(close, 20) * zscore(volume, 20)" - price-volume confirmation

Return ONLY valid JSON:
{
  "hypothesis": "One sentence explaining the trading logic",
  "dsl": "actual_dsl_code"
}
"""


class FactorResearchAgent:
    def __init__(self):
        self.iteration = 0
        
    def propose_factor(self, history_summary: str | None = None) -> Dict[str, Any]:
        self.iteration += 1
        
        # Rotate through different themes
        themes = [
            "Create a momentum factor using price changes over different timeframes.",
            "Create a mean reversion factor using zscore or distance from moving average.",
            "Create a volatility-based factor. Low volatility stocks often outperform.",
            "Create a volume-based factor detecting unusual trading activity.",
            "Combine price momentum with volume confirmation.",
            "Use ts_rank to find stocks at new highs/lows relative to their history.",
            "Create a contrarian factor that profits when stocks reverse.",
            "Normalize factors using zscore to make them comparable across stocks.",
        ]
        
        theme = themes[self.iteration % len(themes)]
        
        user_prompt = f"{theme}\n\nBe creative but use proven patterns as inspiration.\n"
        if history_summary:
            user_prompt += f"\nPrevious best factors:\n{history_summary}\nTry variations or combinations of these.\n"

        messages = [
            {"role": "system", "content": FACTOR_SYSTEM_PROMPT},
            {"role": "user", "content": user_prompt},
        ]
        
        raw = ollama_client.chat(messages, temperature=0.8)  # High creativity
        
        try:
            if "```json" in raw:
                raw = raw.split("```json").split("```")[1]
            elif "```" in raw:
                raw = raw.split("```")[1].split("```")[0]
            data = json.loads(raw.strip())
        except Exception as e:
            print(f"Warning: Failed to parse LLM response: {e}")
            # Use proven fallback factors
            fallback_factors = [
                {"hypothesis": "Medium-term momentum", "dsl": "pct_change(close, 20)"},
                {"hypothesis": "Mean reversion", "dsl": "zscore(close, 20)"},
                {"hypothesis": "Inverse volatility", "dsl": "1 / (rolling_std(pct_change(close, 1), 20) + 0.01)"},
                {"hypothesis": "Volume surge", "dsl": "zscore(volume, 20)"},
                {"hypothesis": "Risk-adjusted momentum", "dsl": "pct_change(close, 10) / rolling_std(pct_change(close, 1), 20)"},
            ]
            data = random.choice(fallback_factors)
        
        return data
