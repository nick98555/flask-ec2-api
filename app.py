from flask import Flask, jsonify

app = Flask(__name__)

@app.route("/")
def index():
    return "Welcome to the Flask API!"

@app.route("/api/status")
def status():
    return jsonify({
        "status": "ok",
        "message": "API is running!"
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
