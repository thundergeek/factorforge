#!/bin/bash
set -euo pipefail

echo "🚀 FactorForge Installer"

if ! command -v docker &> /dev/null; then
    echo "❌ Docker not found. Install from https://www.docker.com/get-started"
    exit 1
fi

if ! docker info &> /dev/null; then
    echo "❌ Docker not running. Start Docker and try again."
    exit 1
fi

echo "✅ Docker found"

if [ -d "factorforge" ]; then
    cd factorforge && git pull
else
    git clone https://github.com/YOURUSERNAME/factorforge.git && cd factorforge
fi

echo "🔨 Building..."
docker compose up -d --build

sleep 10
docker exec factorforge-ollama ollama pull llama3.2:3b 2>/dev/null || true

echo "✅ Done! Dashboard: http://localhost:8050"
