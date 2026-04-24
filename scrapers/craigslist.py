"""Craigslist via RSS. Hits a handful of big metros; add more in CITIES."""
import feedparser
from config import USER_AGENT

SOURCE = "Craigslist"

# Feed format: https://<city>.craigslist.org/search/cta?query=audi+r8&auto_transmission=1&format=rss
# auto_transmission=1 is CL's code for "manual" (yes, confusingly named).
CITIES = [
    "losangeles", "sfbay", "newyork", "chicago", "miami", "dallas", "houston",
    "seattle", "boston", "phoenix", "denver", "atlanta", "sandiego", "austin",
    "portland", "lasvegas", "saltlakecity",
]

def scrape():
    results = []
    for city in CITIES:
        url = (f"https://{city}.craigslist.org/search/cta"
               f"?query=audi+r8&auto_transmission=1&format=rss")
        try:
            feed = feedparser.parse(url, agent=USER_AGENT)
        except Exception as e:
            print(f"[CL:{city}] feed error: {e}")
            continue
        for entry in feed.entries:
            title = entry.get("title", "")
            link = entry.get("link", "")
            desc = entry.get("summary", "") or ""
            if not title or not link:
                continue
            results.append({
                "id": f"cl:{link}",
                "url": link,
                "title": title,
                "description": desc,
                "miles": None,
                "source": f"{SOURCE} ({city})",
            })
    return results
