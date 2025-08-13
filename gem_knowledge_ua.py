# -*- coding: utf-8 -*-
"""gem_knowledge_ua.py — Українська база знань та вказівки.
Призначення:
- Дати боту чіткі системні вказівки українською.
- Забезпечити офіційний збір SERP-даних через Google CSE API.
- Побудувати чернетку структури H1–H6 за результатами SERP.
- Контролювати якість: унікальність, “водність”, експертність, правдивість.

Налаштування:
1) Створи Google Programmable Search Engine (CSE) і включи весь веб.
2) Отримай GOOGLE_API_KEY і GOOGLE_CSE_CX та встанови їх як змінні оточення.
3) Викликай функції з цього модуля, передаючи тему/ключі, мову ('uk') і країну ('UA').

Цей модуль НЕ виконує неофіційних скрейпінг-запитів і не порушує ToS.
"""

from typing import List, Dict, Tuple
from collections import Counter
import difflib
import re

from common_google_cse import GoogleCSE, top_titles, top_snippets, propose_structure_from_serp

INSTRUCTIONS_UA = """
Ти — багатомовний SEO-копірайтер і контент-стратег, що працює за принципом Frase.
Завдання: аналізувати ТЗ, виконувати SERP-аналіз у вказаній країні, пропонувати структуру H1–H6
і писати унікальний, експертний, правдивий текст українською мовою без “води”, використовуючи лише релевантні ринку ключі.

Алгоритм (чек-ліст):
[ ] 1) Аналіз ТЗ: тема, ключі, мова=uk, ринок/країна (UA), аудиторія, стиль/тон.
[ ] 2) SERP-аналіз (Google CSE, hl=uk, gl=UA, cr=countryUA): зібрати топ-заголовки та описи.
[ ] 3) Структура: запропонувати H1–H6 на основі SERP; коротко пояснити зміст кожного розділу.
[ ] 4) Написання: інтегрувати ключі природно, уникати “води”, забезпечити унікальність і правдивість фактів.
[ ] 5) Фінальна перевірка: структура збережена, ключі релевантні ринку, вода ≤ 15%, унікальність ≥ 90%.
Формат відповіді: 1) Чек-ліст (✅/❌), 2) Пропозиція структури, 3) Текст (після апрува).
"""

def serp_research_ua(query: str, num:int=10) -> Dict:
    cse = GoogleCSE()
    items, raw = cse.search(query, hl="uk", gl="UA", cr="countryUA", num=num)
    titles = top_titles(items)
    snippets = top_snippets(items)
    struct = propose_structure_from_serp(query, titles, snippets)
    return { "query": query, "titles": titles, "snippets": snippets, "structure": struct, "raw": raw }

def wateriness_score(text: str) -> float:
    """Оціночний індикатор "води": частка стоп-слів і порожніх фраз."""
    stop = set("""це як також тому лише дуже якщо або коли які який яка що щоб та і але вже ну от тобто мабуть наче просто зокрема взагалі""".split())
    words = re.findall(r"\w+", text.lower(), flags=re.UNICODE)
    if not words: return 0.0
    water = sum(1 for w in words if w in stop)
    return round(100.0 * water / len(words), 2)

def uniqueness_ratio(text: str, references: List[str]) -> float:
    """Груба оцінка унікальності: порівняння з еталонними текстами (Левенштейн/SequenceMatcher)."""
    if not references: return 100.0
    best = 0.0
    for ref in references:
        sim = difflib.SequenceMatcher(None, text, ref).ratio()
        best = max(best, sim)
    return round(100.0 * (1.0 - best), 2)

def propose_structure_ua(query: str):
    data = serp_research_ua(query)
    return data["structure"]
