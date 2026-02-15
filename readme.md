cat > README.md << 'EOF'
# FactorForge ⚒️

**LLM-powered alpha factor discovery via genetic evolution**

FactorForge uses local LLMs (via Ollama) to propose trading factor hypotheses, backtests them on historical price data, and evolves better factors across generations. Results are displayed in a real-time web dashboard.

> **Disclaimer:** This is a research/educational tool. Not financial advice. No guarantee of profitable trading.

---

## System Requirements

### Operating System
**Supported:**
- Linux x86_64 (Ubuntu 22.04/24.04, Debian 12, Fedora 39+, Bazzite)
- macOS (Intel/Apple Silicon - CPU only, no GPU acceleration)
- Windows 10/11 (via WSL2 - see Windows notes below)

**Recommended:** Linux with NVIDIA GPU (RTX 2060 or better)

### Hardware
**Minimum (CPU-only):**
- 4 CPU cores
- 8 GB RAM
- 20 GB disk space

**Recommended (GPU-accelerated):**
- NVIDIA GPU with 6+ GB VRAM (RTX 2060, RTX 3060, RTX 4060, etc.)
- 16 GB RAM
- 50 GB disk space

### Software Prerequisites
**Required:**
- Git
- Docker Engine 24.0+ (Linux) or Docker Desktop (Mac/Windows)
- Docker Compose v2 (usually included as `docker compose`)

**Optional (for GPU acceleration):**
- NVIDIA GPU drivers (535+ recommended)
- NVIDIA Container Toolkit (for Docker GPU support)

---

## Installation

### Step 1: Install Prerequisites

#### Ubuntu/Debian
```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Git and Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Add your user to docker group
sudo usermod -aG docker $USER
newgrp docker

# Verify Docker works
docker run --rm hello-world
