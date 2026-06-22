
import subprocess, time, os

def display_plan(data):

    print(f"  Running  : {data.get('command', '')}\n  Action   : {data.get('explanation', '')}\n  Risk     : {data.get('risk', 'low').upper()}\n")

def run(command, timeout=120, cwd=None):

    start = time.time()

    try:

        res = subprocess.run(command, shell=True, capture_output=True, text=True, timeout=timeout, cwd=cwd)

        return {"returncode": res.returncode, "stdout": res.stdout, "stderr": res.stderr, "duration_seconds": round(time.time()-start, 2)}

    except Exception as e:

        return {"returncode": -1, "stdout": "", "stderr": str(e), "duration_seconds": timeout}

