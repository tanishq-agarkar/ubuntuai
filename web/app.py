
import sys, os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from flask import Flask, render_template, jsonify, request

from flask_socketio import SocketIO, emit

from core import llm, executor, logger, os_metrics



app = Flask(__name__, template_folder="templates")

app.config["SECRET_KEY"] = os.urandom(24)

socketio = SocketIO(app, cors_allowed_origins="*")



@app.route("/")

def index(): return render_template("index.html")



@app.route("/api/status")

def status(): return jsonify({"ollama_ok": True, "snapshot": os_metrics.full_snapshot()})



@socketio.on("message")

def handle_msg(data):

    txt = data.get("text","")

    if data.get("confirmed") and data.get("pending_command"):

        res = executor.run(data["pending_command"])

        sum_txt = llm.summarise(txt, data["pending_command"], res["returncode"], res["stdout"], res["stderr"])

        emit("response", {"text": sum_txt, "command": data["pending_command"], "stdout": res["stdout"], "stderr": res["stderr"], "returncode": res["returncode"], "duration": res["duration_seconds"]})

        return

    plan, raw = llm.interpret(txt)

    if not plan.get("command"):

        emit("response", {"text": plan.get("explanation", "Could not understand.")})

    else:

        emit("plan", {"command": plan["command"], "explanation": plan["explanation"], "risk": plan.get("risk","low"), "original_request": txt})



if __name__ == "__main__":

    socketio.run(app, host="0.0.0.0", port=5000, allow_unsafe_werkzeug=True)

