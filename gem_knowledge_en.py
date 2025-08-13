# -*- coding: utf-8 -*-
"""gem_knowledge_en.py — English knowledge base and instructions.
Purpose:
- Provide strict system guidance in English.
- Fetch SERP data via Google Custom Search API (official).
- Build an H1–H6 skeleton from SERP signals.
- Run lightweight quality checks (uniqueness, wateriness, factuality prompts).

Setup:
1) Create a Google Programmable Search Engine (CSE) covering the web.
2) Obtain GOOGLE_API_KEY and GOOGLE_CSE_CX and set as environment variables.
3) Call functions with topic/keywords, language='en', market='US' (or as needed).

No scraping. Only official Google APIs are used.
"""

from typing import List, Dict, Tuple
from collections import Counter
import difflib
import re

from common_google_cse import GoogleCSE, top_titles, top_snippets, propose_structure_from_serp

INSTRUCTIONS_EN = """
You are a multilingual SEO writer operating in a Frase-like workflow.
Goal: analyze the brief, run market-specific SERP research, propose an H1–H6 outline,
then write unique, expert, factually correct copy in English with minimal fluff,
using only market-relevant keywords.

Checklist:
[ ] 1) Brief analysis: topic, keywords, language=en, market/country (e.g., US), audience, style/tone.
[ ] 2) SERP research (Google CSE; hl=en, gl=US, cr=countryUS): collect top titles and snippets.
[ ] 3) Outline: propose H1–H6 based on SERP; add one-line purpose per section.
[ ] 4) Drafting: integrate keywords naturally, avoid fluff, ensure uniqueness and factual accuracy.
[ ] 5) Final QA: outline preserved, keywords market-relevant, fluff ≤ 15%, uniqueness ≥ 90%.
Response format: 1) Checklist (✅/❌), 2) Outline, 3) Draft (after approval).
"""

def serp_research_en(query: str, country:str="US", num:int=10) -> Dict:
    cse = GoogleCSE()
    items, raw = cse.search(query, hl="en", gl=country, cr=f"country{country}", num=num)
    titles = top_titles(items)
    snippets = top_snippets(items)
    struct = propose_structure_from_serp(query, titles, snippets)
    return { "query": query, "titles": titles, "snippets": snippets, "structure": struct, "raw": raw }

def wateriness_score(text: str) -> float:
    stop = set("""this that also very just then only about which while where when really actually basically however moreover furthermore overall hence thus""".split())
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

def propose_structure_en(query: str):
    data = serp_research_en(query)
    return data["structure"]
