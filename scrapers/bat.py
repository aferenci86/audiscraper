"""Bring a Trailer: search both live auctions and results pages for R8 listings."""
from bs4 import BeautifulSoup
from scrapers.http import fetch

SOURCE = "BaT"
SEARCH_URLS = [
    "https://bringatrailer.com/audi/r8/",
    "https://bringatrailer.com/auctions/?q=audi+r8+manual",
]


def scrape():
    results = []
    seen_urls = set()
    for url in SEARCH_URLS:
        try:
            html = fetch(url).text
        except Exception as e:
            print(f"[BaT] fetch failed for {url}: {e}")
            continue

        soup = BeautifulSoup(html, "html.parser")
        # BaT uses anchor tags with class "auctions-item-title" or similar; fall back to any link to an auction
        for a in soup.select("a[href*='/listing/'], a.auctions-item-title"):
            href = a.get("href", "")
            if not href or "/listing/" not in href:
                continue
            if href in seen_urls:
                continue
            seen_urls.add(href)

            title = a.get_text(strip=True)
            # Listing card context — pull surrounding text for description
            card = a.find_parent(["div", "article", "li"]) or a
            desc = card.get_text(" ", strip=True)[:500]

            # Skip the big generic "results" blurb links that aren't real listings
            if not title or len(title) < 10:
                continue

            results.append({
                "id": f"bat:{href}",
                "url": href,
                "title": title,
                "description": desc,
                "miles": None,
                "source": SOURCE,
            })
    return results
