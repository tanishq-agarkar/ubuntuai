#!/bin/bash

set -e



echo "Installing UbuntuAI..."



sudo apt update



sudo apt install -y \

    git \

    wget \

    curl \

    cmake \

    build-essential \

    python3 \

    python3-pip



pip3 install --user -r requirements.txt



if [ ! -d "$HOME/llama.cpp" ]; then

    git clone https://github.com/ggml-org/llama.cpp ~/llama.cpp

fi



cd ~/llama.cpp



cmake -B build

cmake --build build -j$(nproc)



mkdir -p ~/models



if [ ! -f ~/models/llama32-1b.gguf ]; then

    wget \

https://huggingface.co/bartowski/Llama-3.2-1B-Instruct-GGUF/resolve/main/Llama-3.2-1B-Instruct-Q4_K_M.gguf \

-O ~/models/llama32-1b.gguf

fi



chmod +x scripts/*.sh



echo "Installation complete."
