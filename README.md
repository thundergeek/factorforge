# FactorForge

AI discovers profitable trading factors automatically using local LLMs.

## Inspiration

This project is inspired by the research paper:

**[QuantaAlpha: An Evolutionary Framework for LLM-Driven Alpha Mining](https://arxiv.org/abs/2602.07085)**

The paper proposes using evolutionary algorithms (mutation and crossover) with LLMs to discover robust trading signals. FactorForge adapts these concepts into a lightweight, open-source tool that runs entirely on your own hardware with local LLMs.

## Installation (3 steps)

1. Install Docker: https://www.docker.com/get-started
   - On Bazzite/Fedora: Podman is pre-installed
2. Run: `curl -fsSL https://raw.githubusercontent.com/thundergeek/factorforge/main/install.sh | bash`
3. Open: http://localhost:8050

## Usage

- Add symbols (comma-separated): `AAPL,MSFT,GOOGL,AMZN,NVDA,TSLA,JPM,BAC,V,MA`
- Set Generations: `10`, Population: `20`
- Click **Start Evolution**

Results save to `data/results/factor_results.csv`

## How It Works

1. LLM proposes factor ideas (e.g., "momentum", "mean reversion")
2. Generates DSL code: `pct_change(close, 20)`
3. Backtests on historical stock data
4. Computes metrics: IC (correlation), Sharpe ratio, returns
5. Best factors evolve across generations (genetic algorithm)

## Troubleshooting

- **View logs:** `docker compose logs -f factorforge` (or `podman-compose`)
- **Stop:** `docker compose down`
- **Update:** `git pull && docker compose up -d --build`

## Requirements

- Docker or Podman
- 8GB RAM minimum (16GB recommended)
- 20GB disk space
- Optional: NVIDIA GPU with 6+ GB VRAM

## Attribution

Built with AI assistance from [Perplexity AI](https://www.perplexity.ai) and manually tested/validated.

Inspired by research from:
- Paper: [QuantaAlpha: An Evolutionary Framework for LLM-Driven Alpha Mining](https://arxiv.org/abs/2602.07085)
- HuggingFace: https://huggingface.co/papers/2602.07085

## License

MIT

## Disclaimer

**Research tool only. Not financial advice. Past performance ≠ future results.**
