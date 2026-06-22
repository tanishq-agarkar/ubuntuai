
#!/bin/bash

set -e

GREEN='\033[0;32m'

YELLOW='\033[1;33m'

RED='\033[0;31m'

BLUE='\033[0;34m'

NC='\033[0m'

info()    { echo -e "${GREEN}[INFO]${NC}  $1"; }

warn()    { echo -e "${YELLOW}[WARN]${NC}  $1"; }

error()   { echo -e "${RED}[ERROR]${NC} $1"; exit 1; }

section() { echo -e "\n${BLUE}══════════════════════════════════════${NC}\n${BLUE}  $1${NC}\n${BLUE}══════════════════════════════════════${NC}\n"; }



section "Step 1: Installing system packages"

sudo apt-get update -qq && sudo apt-get install -y build-essential cmake git wget unzip python3 python3-pip curl

info "System packages installed."



section "Step 2: Installing Python packages"

pip3 install --break-system-packages requests flask flask-socketio psutil 2>/dev/null || pip3 install requests flask flask-socketio psutil

info "Python packages installed."



section "Step 3: Building llama.cpp"

cd ~

if [ ! -d "llama.cpp" ]; then git clone https://github.com/ggml-org/llama.cpp; fi

cd ~/llama.cpp

if [ ! -f "build/bin/llama-server" ]; then

  rm -rf build

  cmake -B build -DCMAKE_BUILD_TYPE=Release -DLLAMA_CURL=OFF -DLLAMA_BUILD_TOOLS=OFF -DCMAKE_POLICY_DEFAULT_CMP0048=NEW > /tmp/cmake_config.log 2>&1

  cmake --build build -j$(nproc) 2>&1 | tee /tmp/llama_build.log | grep -E "^\[|error:|Error" || true

  if [ ! -f "build/bin/llama-server" ]; then error "Build failed. Check /tmp/llama_build.log"; fi

fi

info "llama.cpp built successfully."



section "Step 4: Downloading LLM model"

mkdir -p ~/models

MODEL_PATH="$HOME/models/llama32-1b.gguf"

if [ ! -f "$MODEL_PATH" ]; then

  wget -q --show-progress "https://huggingface.co/bartowski/Llama-3.2-1B-Instruct-GGUF/resolve/main/Llama-3.2-1B-Instruct-Q4_K_M.gguf" -O "$MODEL_PATH"

fi

info "Model ready."

