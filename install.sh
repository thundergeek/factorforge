#!/bin/bash
set -euo pipefail

echo "🚀 FactorForge Installer"
echo

# Check for Docker or Podman
if command -v docker &> /dev/null; then
    DOCKER_CMD="docker"
elif command -v podman &> /dev/null; then
    DOCKER_CMD="podman"
    alias docker=podman
else
    echo "❌ Neither Docker nor Podman found"
    echo "On Bazzite: Podman is pre-installed"
    echo "On other systems: Install Docker from https://www.docker.com/get-started"
    exit 1
fi

echo "✅ Using $DOCKER_CMD"

if ! $DOCKER_CMD info &> /dev/null; then
    echo "❌ $DOCKER_CMD daemon not running"
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
echo "🔨 Building containers (this may take a few minutes)..."
$DOCKER_CMD compose up -d --build

echo
echo "⏳ Waiting for services to start..."
sleep 10

echo "📥 Downloading LLM model (llama3.2:3b)..."
$DOCKER_CMD exec factorforge-ollama ollama pull llama3.2:3b

echo
echo "✅ Done! Dashboard: http://localhost:8050"
echo
echo "Useful commands:"
echo "  View logs:  $DOCKER_CMD compose logs -f factorforge"
echo "  Stop:       $DOCKER_CMD compose down"
