from flask import Flask, jsonify, request
from googleapiclient.discovery import build
import os

# Імпортуємо бази знань
import gem_knowledge_en as kn_en
import gem_knowledge_ru as kn_ru
import gem_knowledge_ua as kn_ua

app = Flask(__name__)

# Читаємо API ключ і Search Engine ID з Environment Variables
API_KEY = os.getenv("GOOGLE_API_KEY")
CSE_ID = os.getenv("GOOGLE_CSE_ID")

if not API_KEY or not CSE_ID:
    raise ValueError("Не задано GOOGLE_API_KEY або GOOGLE_CSE_ID в Environment Variables")

# Маршрут для перевірки роботи
@app.route("/")
def home():
    return jsonify({
        "status": "ok",
        "message": "Сервер працює на Render 🚀",
        "google_api_key": API_KEY[:6] + "*****",
        "cse_id": CSE_ID
    })

# Маршрут для Google Search
@app.route("/search")
def google_search():
    query = request.args.get("q")
    if not query:
        return jsonify({"error": "Не задано параметр q"}), 400

    service = build("customsearch", "v1", developerKey=API_KEY)
    results = service.cse().list(q=query, cx=CSE_ID).execute()
    return jsonify(results)

# Маршрут для бази знань
@app.route("/knowledge")
def get_knowledge():
    return jsonify({
        "en": kn_en.knowledge_base,
        "ru": kn_ru.knowledge_base,
        "ua": kn_ua.knowledge_base
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

