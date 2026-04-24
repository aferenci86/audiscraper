"""KSL Cars (Utah) search for R8."""
from bs4 import BeautifulSoup
from scrapers.http import fetch

SOURCE = "KSL"
# KSL's search URL uses `makeModel` combos. Cast a wide net; filter in Python.
SEARCH_URL = "https://cars.ksl.com/search/keyword/audi%20r8"


def scrape():
    try:
        html = fetch(SEARCH_URL).text
    except Exception as e:
        print(f"[KSL] fetch failed: {e}")
        return []

    soup = BeautifulSoup(html, "html.parser")
    results = []
    for a in soup.select("a[href*='/listing/']"):
        href = a.get("href", "")
        if not href:
            continue
        if not href.startswith("http"):
            href = "https://cars.ksl.com" + href
        title = a.get_text(" ", strip=True)
        if not title or len(title) < 6:
            continue
        card = a.find_parent(["div", "article", "li"]) or a
        desc = card.get_text(" ", strip=True)[:600]
        results.append({
            "id": f"ksl:{href}",
            "url": href,
            "title": title,
            "description": desc,
            "miles": None,
            "source": SOURCE,
        })
    dedup = {r["url"]: r for r in results}
    return list(dedup.values())
