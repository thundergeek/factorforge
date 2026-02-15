# FactorForge

AI discovers profitable trading factors automatically using local LLMs.

## Installation (3 steps)

1. Install Docker: https://www.docker.com/get-started
2. Run: curl -fsSL https://raw.githubusercontent.com/thundergeek/factorforge/main/install.sh | bash
3. Open: http://localhost:8050

## Usage

Add symbols (comma-separated): AAPL,MSFT,GOOGL,AMZN,NVDA,TSLA,JPM,BAC,V,MA
Set Generations: 10, Population: 20
Click Start Evolution

Results save to data/results/factor_results.csv

## Troubleshooting

View logs: docker compose logs -f factorforge
Stop: docker compose down
Update: git pull && docker compose up -d --build

## Requirements

- Docker
- 8GB RAM minimum
- 20GB disk space
- Optional: NVIDIA GPU

## Disclaimer

Research tool only. Not financial advice.
