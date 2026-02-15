#!/bin/bash
set -euo pipefail

echo "🚀 FactorForge Installer"
echo

# Check for Docker or Podman
if command -v docker &> /dev/null && docker info &> /dev/null; then
    DOCKER_CMD="docker"
    COMPOSE_CMD="docker compose"
elif command -v podman &> /dev/null; then
    DOCKER_CMD="podman"
    # Try native podman compose first, fall back to podman-compose
    if podman compose version &> /dev/null; then
        COMPOSE_CMD="podman compose"
    elif command -v podman-compose &> /dev/null; then
        COMPOSE_CMD="podman-compose"
    else
        echo "❌ podman-compose not found. Installing..."
        pip3 install --user podman-compose
        COMPOSE_CMD="podman-compose"
    fi
else
    echo "❌ Neither Docker nor Podman found"
    exit 1
fi

echo "✅ Using $DOCKER_CMD"
echo

if [ -d "factorforge" ]; then
    echo "📦 Updating existing repository..."
    cd factorforge && git pull --verbose
else
    echo "📦 Cloning repository..."
    git clone --progress https://github.com/thundergeek/factorforge.git
    cd factorforge
fi

echo
echo "🔨 Building containers (this may take a few minutes)..."
$COMPOSE_CMD up -d --build

echo
echo "⏳ Waiting for services to start..."
sleep 10

echo "📥 Downloading LLM model (llama3.2:3b)..."
$DOCKER_CMD exec factorforge-ollama ollama pull llama3.2:3b

echo
echo "✅ Done! Dashboard: http://localhost:8050"
echo
echo "Useful commands:"
echo "  View logs:  $COMPOSE_CMD logs -f factorforge"
echo "  Stop:       $COMPOSE_CMD down"
