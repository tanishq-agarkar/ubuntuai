
import os, json

from datetime import datetime

LOG_FILE = os.path.expanduser("~/.ubuntuai/history.jsonl")

def log(user_request, command, risk, result):

    os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)

    try:

        with open(LOG_FILE, "a") as f:

            f.write(json.dumps({"timestamp": datetime.now().isoformat(), "request": user_request, "command": command, "returncode": result.get("returncode")}) + "\n")

    except: pass

def recent(n=10):

    try:

        with open(LOG_FILE) as f: return [json.loads(l) for l in f if l.strip()][-n:]

    except: return []

