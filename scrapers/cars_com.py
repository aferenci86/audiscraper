"""Cars.com search for Audi R8 manual under 60k miles."""
from bs4 import BeautifulSoup
from scrapers.http import fetch

SOURCE = "Cars.com"
SEARCH_URL = (
    "https://www.cars.com/shopping/results/"
    "?makes[]=audi&models[]=audi-r8"
    "&maximum_mileage=60000&transmission=manual&stock_type=used"
)


def scrape():
    try:
        html = fetch(SEARCH_URL).text
    except Exception as e:
        print(f"[Cars.com] fetch failed: {e}")
        return []

    soup = BeautifulSoup(html, "html.parser")
    results = []
    for card in soup.select("div.vehicle-card, a.vehicle-card-link"):
        link = card if card.name == "a" else card.find("a", href=True)
        if not link:
            continue
        href = link.get("href", "")
        if not href:
            continue
        if not href.startswith("http"):
            href = "https://www.cars.com" + href
        title = card.get_text(" ", strip=True)[:200]
        if len(title) < 8:
            continue
        results.append({
            "id": f"carscom:{href.split('?')[0]}",
            "url": href,
            "title": title,
            "description": card.get_text(" ", strip=True)[:600],
            "miles": None,
            "source": SOURCE,
        })
    dedup = {r["id"]: r for r in results}
    return list(dedup.values())
