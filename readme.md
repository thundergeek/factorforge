cat > README.md << 'EOF'
# FactorForge ⚒️
LLM-driven alpha factor discovery that **forges** candidate trading signals (factors) and evaluates them via an evolution loop with backtests and a web dashboard.

> Disclaimer: This project is for research/education. It is not financial advice and does not guarantee profitable trading outcomes.

---

## What it does
- Uses a local LLM (via **Ollama**) to propose factor hypotheses + DSL expressions
- Evaluates factors on historical OHLCV data and computes metrics (IC, Sharpe, drawdown, etc.)
- Iterates across generations/agents and writes results to `data/results/factor_results.csv` and `.json`
- Provides a lightweight dashboard at `http://localhost:8050`

---

## Requirements
- Docker
- (Optional but recommended) NVIDIA GPU + drivers
- If using GPU in Docker: NVIDIA Container Toolkit / GPU runtime support
- Ollama running locally (recommended)

---

## Quick start (Docker)
### 1) Start Ollama (host)
Install and run Ollama on the host machine, then pull a model:

```bash
ollama serve
ollama pull llama3.1:8b
