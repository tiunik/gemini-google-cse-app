# Gemini Google CSE App

Це веб-додаток, який використовує Google Custom Search API для пошуку інформації українською, англійською та російською мовами.

## Файли проекту
- `app.py` — основний Flask-додаток.
- `common_google_cse.py` — модуль з налаштуваннями API.
- `gem_knowledge_ua.py`, `gem_knowledge_en.py`, `gem_knowledge_ru.py` — файли знань для відповідних мов.
- `requirements.txt` — список залежностей.

## Налаштування
1. Створи API ключ у [Google Cloud Console](https://console.cloud.google.com/).
2. Створи Google Custom Search Engine (CSE) та збережи його ID.
3. Додай ці значення у `common_google_cse.py`.

## Запуск
```bash
pip install -r requirements.txt
python app.py
