import os
import platform
import socket
import time
import sqlite3
import shutil
import psutil
from flask import Flask, jsonify, request, abort, render_template

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

# Auto-log all /api/* requests
@app.before_request
def log_all_requests():
    if request.path.startswith("/api/") and request.path != "/api/logs":
        conn = sqlite3.connect("apilogs.db")
        c = conn.cursor()
        c.execute("INSERT INTO logs (timestamp, endpoint, ip_address) VALUES (?, ?, ?)", (
            time.strftime("%Y-%m-%d %H:%M:%S"),
            request.path,
            request.remote_addr
        ))
        conn.commit()
        conn.close()

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

# @app.route("/api/logs")
# def get_logs():
    # limit = request.args.get("limit", default=10, type=int)
    # conn = sqlite3.connect("apilogs.db")
    # c = conn.cursor()
    # c.execute("SELECT timestamp, endpoint, ip_address FROM logs ORDER BY id DESC LIMIT ?", (limit,))
    # rows = c.fetchall()
    # conn.close()
    # return jsonify([
        # {"timestamp": r[0], "endpoint": r[1], "ip_address": r[2]} for r in rows
    # ])
    
# # clears all logs
# @app.route("/api/logs/clear", methods=["POST"])
# def clear_logs():
    # conn = sqlite3.connect("apilogs.db")
    # c = conn.cursor()
    # c.execute("DELETE FROM logs")
    # conn.commit()
    # conn.close()
    # return jsonify({"status": "success", "message": "All logs cleared."})

# @app.route("/api/syslogs")
# def get_syslogs():
    # conn = sqlite3.connect("syslogs.db")
    # c = conn.cursor()
    # c.execute("SELECT ip, user, timestamp FROM failed_logins ORDER BY timestamp DESC LIMIT 100")
    # rows = c.fetchall()
    # conn.close()
    # return jsonify([
        # {"ip": row[0], "user": row[1], "timestamp": row[2]}
        # for row in rows
    # ])    
 
@app.route("/dashboard/apilogs")
def api_logs_dashboard():
    conn = sqlite3.connect("apilogs.db")
    c = conn.cursor()
    c.execute("SELECT timestamp, endpoint FROM logs ORDER BY timestamp DESC LIMIT 100")
    logs = c.fetchall()
    conn.close()
    return render_template("apilogs.html", logs=logs)

@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")
    
def init_db():
    conn = sqlite3.connect("apilogs.db")
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            endpoint TEXT,
            ip_address TEXT
        )
    """)
    conn.commit()
    conn.close()

init_db()    
    
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)