from flask import Flask, jsonify, request
from googleapiclient.discovery import build
import os


# Імпорт баз знань
import gem_knowledge_en as kn_en
import gem_knowledge_ru as kn_ru
import gem_knowledge_ua as kn_ua

app = Flask(__name__)

# Читаємо API ключ і Search Engine ID з .env або Environment Variables
API_KEY = os.getenv("GOOGLE_API_KEY")
CSE_ID = os.getenv("GOOGLE_CSE_ID")

if not API_KEY or not CSE_ID:
    raise ValueError("Не задано GOOGLE_API_KEY або GOOGLE_CSE_ID в Environment Variables")

# Ендпоінт для перевірки
@app.route("/")
def home():
    return jsonify({
        "cse_id": CSE_ID,
        "google_api_key": API_KEY,
        "message": "Сервер працює 🚀",
        "status": "ok"
    })

# Ендпоінт для бази знань
@app.route("/knowledge", methods=["GET"])
def get_knowledge():
    lang = request.args.get("lang", "en")
    if lang == "ru":
        return jsonify(kn_ru.knowledge_base)
    elif lang == "ua":
        return jsonify(kn_ua.knowledge_base)
    else:
        return jsonify(kn_en.knowledge_base)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
