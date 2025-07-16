import os
import platform
import socket
import time
from flask import Flask, jsonify

app = Flask(__name__)

@app.route("/")
def index():
    return "Welcome to the Flask API!"

@app.route("/api/status")
def status():
    return jsonify({"status": "ok", "message": "API is running!"})

@app.route("/api/time")
def current_time():
    return jsonify({"time": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())})

@app.route("/api/info")
def system_info():
    return jsonify({
        "hostname": socket.gethostname(),
        "os": platform.system(),
        "os_version": platform.version(),
        "python_version": platform.python_version(),
        "uptime": os.popen("uptime -p").read().strip()
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
