import os
from flask import Flask, jsonify, request
from googleapiclient.discovery import build

# Імпорт баз знань
import gem_knowledge_en
import gem_knowledge_ru
import gem_knowledge_ua

app = Flask(__name__)

API_KEY = os.getenv("GOOGLE_API_KEY")
CSE_ID = os.getenv("GOOGLE_CSE_ID")

@app.route("/")
def home():
    return jsonify({
        "status": "ok",
        "message": "Сервер працює на Render 🚀",
        "google_api_key": API_KEY,
        "cse_id": CSE_ID
    })

@app.route("/search")
def search():
    query = request.args.get("q")
    if not query:
        return jsonify({"error": "Missing query"}), 400

    service = build("customsearch", "v1", developerKey=API_KEY)
    res = service.cse().list(q=query, cx=CSE_ID).execute()
    return jsonify(res)

@app.route("/knowledge")
def knowledge():
    lang = request.args.get("lang", "en").lower()
    if lang == "ru":
        return jsonify(gem_knowledge_ru.knowledge_base)
    elif lang == "ua":
        return jsonify(gem_knowledge_ua.knowledge_base)
    else:
        return jsonify(gem_knowledge_en.knowledge_base)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
