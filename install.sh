#!/bin/bash
set -euo pipefail

echo "🚀 FactorForge Installer"
echo

# Check for Docker or Podman
if command -v docker &> /dev/null && docker info &> /dev/null; then
    DOCKER_CMD="docker"
    COMPOSE_CMD="docker compose"
    echo "✅ Using Docker"
elif command -v podman &> /dev/null; then
    DOCKER_CMD="podman"
    echo "✅ Using Podman"
    
    # Check for compose
    if podman compose version &> /dev/null 2>&1; then
        COMPOSE_CMD="podman compose"
        echo "✅ Podman compose plugin found"
    elif command -v podman-compose &> /dev/null; then
        COMPOSE_CMD="podman-compose"
        echo "✅ podman-compose found"
    else
        echo
        echo "❌ podman-compose not found"
        echo
        echo "Install it with:"
        echo "  pip3 install --user podman-compose"
        echo "  export PATH=\"\$HOME/.local/bin:\$PATH\""
        echo
        read -p "Install now? (y/n) " -n 1 -r
        echo
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            pip3 install --user podman-compose
            export PATH="$HOME/.local/bin:$PATH"
            COMPOSE_CMD="podman-compose"
            echo "✅ Installed podman-compose"
        else
            echo "❌ Cannot proceed without podman-compose"
            exit 1
        fi
    fi
else
    echo "❌ Neither Docker nor Podman found"
    echo
    echo "Install one of:"
    echo "  • Bazzite/Fedora: Podman is pre-installed, try: systemctl --user start podman.socket"
    echo "  • Other Linux: curl -fsSL https://get.docker.com | sh"
    echo "  • Windows/Mac: https://www.docker.com/get-started"
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
