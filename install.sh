#!/bin/bash
set -euo pipefail

echo "🚀 FactorForge Installer"
echo

if command -v docker &> /dev/null && docker info &> /dev/null; then
    DOCKER_CMD="docker"
    COMPOSE_CMD="docker compose"
    echo "✅ Using Docker"
elif command -v podman &> /dev/null; then
    DOCKER_CMD="podman"
    echo "✅ Using Podman"
    
    if podman compose version &> /dev/null 2>&1; then
        COMPOSE_CMD="podman compose"
        echo "✅ Podman compose plugin found"
    elif command -v podman-compose &> /dev/null; then
        COMPOSE_CMD="podman-compose"
        echo "✅ podman-compose found"
    else
        echo
        echo "❌ podman-compose not found"
        echo "Install it with: pip3 install --user podman-compose"
        exit 1
    fi
else
    echo "❌ Neither Docker nor Podman found"
    exit 1
fi

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
echo "🔨 Building containers..."
$COMPOSE_CMD up -d --build

echo
echo "⏳ Waiting for Ollama..."
for i in {1..30}; do
    if $DOCKER_CMD exec factorforge-ollama ollama --version &> /dev/null; then
        echo "✅ Ollama ready"
        break
    fi
    echo -n "."
    sleep 2
done
echo

echo "📥 Downloading model..."
$DOCKER_CMD exec factorforge-ollama ollama pull llama3.2:3b

echo
echo "✅ Done! http://localhost:8050"
