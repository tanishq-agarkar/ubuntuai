
#!/bin/bash

MODE=${1:-cli}

cd ~/ubuntuai

bash scripts/start_llama.sh

if [ "$MODE" = "web" ]; then

  python3 web/app.py

else

  python3 core/agent.py

fi

