# -*- coding: utf-8 -*-
"""common_google_cse.py
Utility helpers shared by language-specific instruction modules.
Requires: Google Custom Search JSON API (official).
Docs: https://developers.google.com/custom-search/v1/overview

Set environment variables before use:
- GOOGLE_API_KEY : your Google API key
- GOOGLE_CSE_CX  : your Programmable Search Engine (CSE) ID

Optional regionalization parameters:
- hl : interface language ('uk','en','ru', etc.)
- gl : country code for results personalization ('UA','US','RU', etc.)
- cr : country restrict (e.g., 'countryUA','countryUS','countryRU')

This module purposefully avoids scraping. Only official Google APIs are used.
"""

import os
import requests
from collections import Counter
from urllib.parse import urlencode
import re

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY", "")
GOOGLE_CSE_CX  = os.getenv("GOOGLE_CSE_CX", "")

class GoogleCSE:
    def __init__(self, api_key: str = None, cx: str = None):
        self.api_key = api_key or GOOGLE_API_KEY
        self.cx = cx or GOOGLE_CSE_CX
        if not self.api_key or not self.cx:
            raise RuntimeError("Set GOOGLE_API_KEY and GOOGLE_CSE_CX environment variables.")

    def search(self, query: str, hl: str = None, gl: str = None, cr: str = None, num: int = 10, start: int = 1):
        """Run a search via Google CSE. Returns parsed items list.
        Parameters map to official API (hl/gl/cr are passed as 'lr'/'gl'/'cr' best-effort).
        Note: 'hl' is not a first-class CSE param; we use 'lr' to bias language results.
        """
        params = {
            "key": self.api_key,
            "cx": self.cx,
            "q": query,
            "num": max(1, min(num, 10)),
            "start": max(1, start)
        }
        if gl:
            params["gl"] = gl.upper()
        if cr:
            params["cr"] = f"country{cr.upper()}" if not cr.lower().startswith("country") else cr
        if hl:
            # Language restrict (e.g., lang_uk, lang_en, lang_ru)
            lang_map = { "uk":"lang_uk", "en":"lang_en", "ru":"lang_ru" }
            lr = lang_map.get(hl.lower())
            if lr:
                params["lr"] = lr

        url = "https://www.googleapis.com/customsearch/v1?" + urlencode(params)
        resp = requests.get(url, timeout=30)
        resp.raise_for_status()
        data = resp.json()
        return data.get("items", []), data

def top_titles(items):
    return [it.get("title","").strip() for it in items if it.get("title")]

def top_snippets(items):
    return [it.get("snippet","").strip() for it in items if it.get("snippet")]

def common_ngrams(titles, min_count=2):
    # Lightweight n-gram frequency from titles to propose subtopics
    tokens = []
    for t in titles:
        t = re.sub(r"[^\w\s-]", " ", t, flags=re.UNICODE)
        tokens.extend([w.lower() for w in t.split() if len(w) > 2])
    grams = []
    for n in (2,3):
        for i in range(len(tokens)-n+1):
            grams.append(" ".join(tokens[i:i+n]))
    from collections import Counter
    cnt = Counter(grams)
    return [g for g,c in cnt.most_common() if c >= min_count]

def propose_structure_from_serp(query, titles, snippets):
    # Very simple structure heuristic
    subs = common_ngrams(titles, min_count=2)[:6]
    structure = [("H1", query)]
    for s in subs:
        structure.append(("H2", s.capitalize()))
    # Fallbacks if too few subtopics
    if len(structure) < 4:
        extra = [t for t in titles[:5] if t]
        for e in extra:
            structure.append(("H2", e))
    return structure
