"""Main entrypoint. Runs all scrapers, filters, dedupes, notifies."""
import traceback

import storage
from filters import matches
import notifier

from scrapers import bat, pcarmarket, ebay, craigslist, ksl, cargurus, autotrader, cars_com

SCRAPERS = [
    ("BaT", bat.scrape),
    ("PCarMarket", pcarmarket.scrape),
    ("eBay", ebay.scrape),
    ("Craigslist", craigslist.scrape),
    ("KSL", ksl.scrape),
    ("CarGurus", cargurus.scrape),
    ("AutoTrader", autotrader.scrape),
    ("Cars.com", cars_com.scrape),
]


def main():
    storage.init()

    all_listings = []
    for name, fn in SCRAPERS:
        try:
            print(f"--- {name} ---")
            listings = fn() or []
            print(f"  raw: {len(listings)}")
            all_listings.extend(listings)
        except Exception:
            print(f"  {name} crashed:")
            traceback.print_exc()

    # Filter
    filtered = [l for l in all_listings if matches(l)]
    print(f"\nFiltered (R8 + V8/V10 + manual + <=60k miles): {len(filtered)}")

    # Dedup against DB
    new_ones = []
    for l in filtered:
        if storage.is_new(l["id"]):
            new_ones.append(l)
            storage.mark_seen(l["id"], l["source"], l["url"], l["title"])

    print(f"New since last run: {len(new_ones)}")
    for l in new_ones:
        miles = l.get("miles")
        ms = f"{miles:,}" if miles else "?"
        print(f"  [{l['source']}] {l['title'][:80]} — {ms}mi — {l['url']}")

    notifier.send(new_ones)


if __name__ == "__main__":
    main()
