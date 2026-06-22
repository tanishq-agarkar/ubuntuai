
import os

import re

import requests



LLAMA_URL = os.environ.get("LLAMA_URL", "http://127.0.0.1:8080")

MODEL_NAME = os.environ.get("AI_AGENT_MODEL", "local")



SYSTEM_INTERPRET = """

You are an Ubuntu terminal assistant.



Convert the user's request into exactly one bash command.



Rules:

- Output ONLY the command.

- No explanations.

- No markdown.

- No code blocks.

- No labels.

- No comments.

- No extra text.



Examples:



User: list directories

Output:

ls -l



User: show current directory

Output:

pwd



User: list files including hidden ones

Output:

ls -la

"""



def check_server():

    try:

        r = requests.get(f"{LLAMA_URL}/health", timeout=5)

        return (True, "Ready")

    except:

        return (False, "Cannot reach server")





def _chat(messages, max_tokens=80):

    r = requests.post(

        f"{LLAMA_URL}/v1/chat/completions",

        json={

            "model": MODEL_NAME,

            "messages": messages,

            "temperature": 0,

            "max_tokens": max_tokens,

            "stream": False

        },

        timeout=60

    )



    return r.json()["choices"][0]["message"]["content"].strip()





def interpret(user_request, history=None):



    messages = [

        {"role": "system", "content": SYSTEM_INTERPRET},

        {"role": "user", "content": user_request}

    ]



    raw = _chat(messages)



    # Remove markdown fences if present

    cmd = raw.replace("```bash", "").replace("```", "").strip()



    # Take only the first line

    cmd = cmd.splitlines()[0].strip()



    return {

        "command": cmd,

        "explanation": "",

        "risk": "low",

        "needs_sudo": False,

        "ask_input": "",

        "multi_step": []

    }, raw





def summarise(user_request, command, returncode, stdout, stderr):

    return ""

