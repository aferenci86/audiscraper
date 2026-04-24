"""CarGurus search page. CG's HTML shifts; this targets the common listing card pattern.
If it stops returning results, their markup changed — inspect a search page and update selectors.
"""
from bs4 import BeautifulSoup
from scrapers.http import fetch

SOURCE = "CarGurus"
# entitySelectingHelper.selectedEntity=d2257 is Audi R8 model id; transmission=205 is manual.
SEARCH_URL = (
    "https://www.cargurus.com/Cars/inventorylisting/viewDetailsFilterViewInventoryListing.action"
    "?sourceContext=carGurusHomePageModel"
    "&entitySelectingHelper.selectedEntity=d2257"
    "&transmission=205"
    "&maxMileage=60000"
)


def scrape():
    try:
        html = fetch(SEARCH_URL).text
    except Exception as e:
        print(f"[CarGurus] fetch failed: {e}")
        return []

    soup = BeautifulSoup(html, "html.parser")
    results = []
    # CG uses data attrs on listing cards
    for card in soup.select("[data-cg-ft='car-blade-listing-title'], div.cg-dealFinder-result-wrap, a[href*='/Cars/link/']"):
        title = card.get_text(" ", strip=True)[:200]
        # Find a link
        if card.name == "a":
            href = card.get("href", "")
        else:
            link = card.find("a", href=True)
            href = link["href"] if link else ""
        if not href:
            continue
        if not href.startswith("http"):
            href = "https://www.cargurus.com" + href
        if len(title) < 8:
            continue
        results.append({
            "id": f"cargurus:{href}",
            "url": href,
            "title": title,
            "description": title,
            "miles": None,
            "source": SOURCE,
        })
    dedup = {r["url"]: r for r in results}
    return list(dedup.values())
