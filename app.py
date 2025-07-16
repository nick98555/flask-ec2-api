import os
import platform
import socket
import time
import shutil
import psutil
from flask import Flask, jsonify

app = Flask(__name__)

@app.route("/")
def index():
    return "Welcome to the Flask API!"

@app.route("/api/status")
def status():
    return jsonify({"status": "ok", "message": "API is running"})

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
        
@app.route("/api/health")
def health_check():
    disk = shutil.disk_usage("/")
    return jsonify({
        "cpu_percent": psutil.cpu_percent(interval=1),
        "ram_percent": psutil.virtual_memory().percent,
        "disk_percent": disk.used / disk.total * 100
    })
    
@app.route("/api/network")
def network_info():
    return jsonify({
        "hostname": socket.gethostname(),
        "ip_address": socket.gethostbyname(socket.gethostname()),
        "interfaces": list(psutil.net_if_addrs().keys()),
        "gateways": psutil.net_if_stats()
    })
    
@app.route("/api/processes")
def top_processes():
    procs = sorted(psutil.process_iter(['pid', 'name', 'memory_percent']),
                   key=lambda p: p.info['memory_percent'],
                   reverse=True)[:5]
    return jsonify([p.info for p in procs])
    
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
