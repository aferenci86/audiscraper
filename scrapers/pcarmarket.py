"""PCarMarket: search page for R8."""
from bs4 import BeautifulSoup
from scrapers.http import fetch

SOURCE = "PCarMarket"
SEARCH_URL = "https://www.pcarmarket.com/auction/search/?query=audi+r8"


def scrape():
    try:
        html = fetch(SEARCH_URL).text
    except Exception as e:
        print(f"[PCarMarket] fetch failed: {e}")
        return []

    soup = BeautifulSoup(html, "html.parser")
    results = []
    # Auction cards typically have links to /auction/<slug>/
    for a in soup.select("a[href*='/auction/']"):
        href = a.get("href", "")
        if not href or "/auction/search" in href:
            continue
        if not href.startswith("http"):
            href = "https://www.pcarmarket.com" + href
        title = a.get_text(strip=True)
        if not title or len(title) < 8:
            continue
        card = a.find_parent(["div", "article", "li"]) or a
        desc = card.get_text(" ", strip=True)[:500]
        results.append({
            "id": f"pcarmarket:{href}",
            "url": href,
            "title": title,
            "description": desc,
            "miles": None,
            "source": SOURCE,
        })
    # Dedup by URL (cards often repeat the link)
    dedup = {}
    for r in results:
        dedup[r["url"]] = r
    return list(dedup.values())
