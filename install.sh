#!/bin/bash
set -euo pipefail

echo "🚀 FactorForge Installer"

# Check for Docker or Podman
if command -v docker &> /dev/null; then
    DOCKER_CMD="docker"
elif command -v podman &> /dev/null; then
    DOCKER_CMD="podman"
    alias docker=podman
    alias docker-compose="podman-compose"
else
    echo "❌ Neither Docker nor Podman found"
    echo "On Bazzite: Podman is pre-installed, try 'podman' directly"
    echo "On other systems: Install Docker from https://www.docker.com/get-started"
    exit 1
fi

echo "✅ Using $DOCKER_CMD"

# Test if it's actually working
if ! $DOCKER_CMD info &> /dev/null; then
    echo "❌ $DOCKER_CMD daemon not running"
    if [ "$DOCKER_CMD" = "podman" ]; then
        echo "Run: systemctl --user start podman.socket"
    else
        echo "Start Docker and try again"
    fi
    exit 1
fi

if [ -d "factorforge" ]; then
    cd factorforge && git pull
else
    git clone https://github.com/YOURUSERNAME/factorforge.git && cd factorforge
fi

echo "🔨 Building..."
$DOCKER_CMD compose up -d --build

sleep 10
$DOCKER_CMD exec factorforge-ollama ollama pull llama3.2:3b 2>/dev/null || true

echo "✅ Done! Dashboard: http://localhost:8050"
