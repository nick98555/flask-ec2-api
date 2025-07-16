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
        "architecture": platform.machine(),
        "python_version": platform.python_version(),
        "uptime": os.popen("uptime -p").read().strip().replace("up ", "")
    })
        
@app.route("/api/health")
def health_check():
    disk = shutil.disk_usage("/")
    return jsonify({
        "cpu_usage_percent": f"{psutil.cpu_percent(interval=1):.1f}%",
        "memory_usage_percent": f"{psutil.virtual_memory().percent:.1f}%",
        "disk_usage_percent": f"{(disk.used / disk.total * 100):.1f}%"
    })
    
@app.route("/api/network")
def network_info():
    interfaces = {}
    for name, addrs in psutil.net_if_addrs().items():
        interfaces[name] = {
            "ip_addresses": [addr.address for addr in addrs if addr.family.name == "AF_INET"]
        }

    stats = {iface: stat.isup for iface, stat in psutil.net_if_stats().items()}

    return jsonify({
        "hostname": socket.gethostname(),
        "interfaces": interfaces,
        "interface_status": stats
    })
    
@app.route("/api/processes")
def top_processes():
    procs = sorted(psutil.process_iter(['pid', 'name', 'memory_percent']),
                   key=lambda p: p.info['memory_percent'],
                   reverse=True)[:5]

    return jsonify([
        {
            "pid": p.info['pid'],
            "name": p.info['name'],
            "memory_percent": f"{p.info['memory_percent']:.2f}%"
        } for p in procs
    ])
    
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
