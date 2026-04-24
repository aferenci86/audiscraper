"""AutoTrader search for Audi R8 manual under 60k miles."""
from bs4 import BeautifulSoup
from scrapers.http import fetch

SOURCE = "AutoTrader"
SEARCH_URL = (
    "https://www.autotrader.com/cars-for-sale/all-cars/audi/r8"
    "?maxMileage=60000&transmissionCode=MAN&searchRadius=0"
)


def scrape():
    try:
        html = fetch(SEARCH_URL).text
    except Exception as e:
        print(f"[AutoTrader] fetch failed: {e}")
        return []

    soup = BeautifulSoup(html, "html.parser")
    results = []
    for a in soup.select("a[href*='/cars-for-sale/vehicledetails'], a[data-cmp='link']"):
        href = a.get("href", "")
        if not href or "vehicledetails" not in href:
            continue
        if not href.startswith("http"):
            href = "https://www.autotrader.com" + href
        card = a.find_parent(["div", "article", "li"]) or a
        title = card.get_text(" ", strip=True)[:200]
        if len(title) < 8:
            continue
        results.append({
            "id": f"autotrader:{href.split('?')[0]}",  # strip tracking params for dedup
            "url": href,
            "title": title,
            "description": card.get_text(" ", strip=True)[:600],
            "miles": None,
            "source": SOURCE,
        })
    dedup = {r["id"]: r for r in results}
    return list(dedup.values())
