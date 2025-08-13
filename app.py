import os
from flask import Flask, jsonify

app = Flask(__name__)

# Читаємо API ключ і Search Engine ID з Environment Variables
API_KEY = os.getenv("GOOGLE_API_KEY")
CSE_ID = os.getenv("GOOGLE_CSE_ID")

if not API_KEY or not CSE_ID:
    raise ValueError("Не задано GOOGLE_API_KEY або GOOGLE_CSE_ID в Environment Variables")

@app.route("/")
def home():
    return jsonify({
        "status": "ok",
        "message": "Сервер працює на Render 🚀",
        "google_api_key": API_KEY[:5] + "*****",  # не показуємо повністю
        "cse_id": CSE_ID
    })

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
