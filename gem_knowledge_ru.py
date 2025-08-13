# -*- coding: utf-8 -*-
"""gem_knowledge_ru.py — Русская база знаний и инструкции.
Назначение:
- Дать боту строгие системные указания на русском.
- Получать SERP-данные через официальный Google CSE API.
- Строить черновик структуры H1–H6 по сигналам SERP.
- Проверять качество: уникальность, "водность", экспертность, правдивость.

Настройка:
1) Создай Programmable Search Engine (CSE) для всего веба.
2) Получи GOOGLE_API_KEY и GOOGLE_CSE_CX и укажи их в переменных окружения.
3) Вызывай функции, передавая тему/ключи, язык='ru' и нужную страну ('RU' или др.).

Только официальные API Google. Без скрейпинга.
"""

from typing import List, Dict, Tuple
from collections import Counter
import difflib
import re

from common_google_cse import GoogleCSE, top_titles, top_snippets, propose_structure_from_serp

INSTRUCTIONS_RU = """
Ты — многоязычный SEO-копирайтер, работающий по схеме Frase.
Цель: проанализировать ТЗ, выполнить SERP-анализ по выбранной стране, предложить структуру H1–H6,
после утверждения — написать уникальный, экспертный и правдивый текст на русском, без "воды",
используя только релевантные рынку ключи.

Чек-лист:
[ ] 1) Анализ ТЗ: тема, ключи, язык=ru, рынок/страна (напр., RU), аудитория, стиль/тон.
[ ] 2) SERP-анализ (Google CSE; hl=ru, gl=RU, cr=countryRU): собрать топ-заголовки и сниппеты.
[ ] 3) Структура: предложить H1–H6 на основе SERP; дать краткие пояснения к разделам.
[ ] 4) Написание: естественно интегрировать ключи, избегать воды, обеспечить уникальность и факт-чекинг.
[ ] 5) Финальная проверка: структура сохранена, ключи релевантны рынку, вода ≤ 15%, уникальность ≥ 90%.
Формат ответа: 1) Чек-лист (✅/❌), 2) Структура, 3) Текст (после апрува).
"""

def serp_research_ru(query: str, country:str="RU", num:int=10) -> Dict:
    cse = GoogleCSE()
    items, raw = cse.search(query, hl="ru", gl=country, cr=f"country{country}", num=num)
    titles = top_titles(items)
    snippets = top_snippets(items)
    struct = propose_structure_from_serp(query, titles, snippets)
    return { "query": query, "titles": titles, "snippets": snippets, "structure": struct, "raw": raw }

def wateriness_score(text: str) -> float:
    stop = set("""это как также очень лишь когда где куда чтобы однако вообще затем иначе просто именно кроме всего прочего например""".split())
    words = re.findall(r"\w+", text.lower(), flags=re.UNICODE)
    if not words: return 0.0
    water = sum(1 for w in words if w in stop)
    return round(100.0 * water / len(words), 2)

def uniqueness_ratio(text: str, references: List[str]) -> float:
    if not references: return 100.0
    best = 0.0
    for ref in references:
        sim = difflib.SequenceMatcher(None, text, ref).ratio()
        best = max(best, sim)
    return round(100.0 * (1.0 - best), 2)

def propose_structure_ru(query: str):
    data = serp_research_ru(query)
    return data["structure"]
