
#!/bin/bash

LLAMA_DIR="$HOME/llama.cpp"

MODEL_PATH="$HOME/models/llama32-1b.gguf"

if curl -s http://127.0.0.1:8080/health &>/dev/null; then

  echo "[llama] Server running."

else

  nohup "$LLAMA_DIR/build/bin/llama-server" -m "$MODEL_PATH" --host 127.0.0.1 --port 8080 -c 2048 -t $(nproc) --temp 0.1 -ngl 0 > /tmp/llama-server.log 2>&1 &

  sleep 4

fi

