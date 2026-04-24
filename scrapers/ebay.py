"""eBay via Browse API. Needs an App ID (free dev account)."""
import base64
import requests
from config import EBAY_APP_ID, REQUEST_TIMEOUT

SOURCE = "eBay"
BROWSE_URL = "https://api.ebay.com/buy/browse/v1/item_summary/search"
TOKEN_URL = "https://api.ebay.com/identity/v1/oauth2/token"


def _get_app_token():
    """Get an application access token using the App ID as both client id and secret.
    If your eBay key is formatted as 'CLIENT_ID:CLIENT_SECRET', split it; otherwise assumes
    user provides it in that form via EBAY_APP_ID.
    """
    if ":" not in EBAY_APP_ID:
        raise RuntimeError("EBAY_APP_ID should be 'clientid:clientsecret'")
    encoded = base64.b64encode(EBAY_APP_ID.encode()).decode()
    r = requests.post(
        TOKEN_URL,
        headers={
            "Authorization": f"Basic {encoded}",
            "Content-Type": "application/x-www-form-urlencoded",
        },
        data={
            "grant_type": "client_credentials",
            "scope": "https://api.ebay.com/oauth/api_scope",
        },
        timeout=REQUEST_TIMEOUT,
    )
    r.raise_for_status()
    return r.json()["access_token"]


def scrape():
    if not EBAY_APP_ID:
        print("[eBay] EBAY_APP_ID not set, skipping")
        return []
    try:
        token = _get_app_token()
    except Exception as e:
        print(f"[eBay] token error: {e}")
        return []

    headers = {
        "Authorization": f"Bearer {token}",
        "X-EBAY-C-MARKETPLACE-ID": "EBAY_US",
    }
    params = {
        "q": "Audi R8 manual",
        "category_ids": "6001",  # "Cars & Trucks"
        "limit": "50",
        "filter": "buyingOptions:{FIXED_PRICE|AUCTION}",
    }
    try:
        r = requests.get(BROWSE_URL, headers=headers, params=params, timeout=REQUEST_TIMEOUT)
        r.raise_for_status()
    except Exception as e:
        print(f"[eBay] search error: {e}")
        return []

    data = r.json()
    items = data.get("itemSummaries", []) or []
    out = []
    for it in items:
        title = it.get("title", "")
        url = it.get("itemWebUrl", "")
        item_id = it.get("itemId", url)
        # eBay sometimes exposes mileage in itemSpecifics but the Browse search doesn't always return them
        out.append({
            "id": f"ebay:{item_id}",
            "url": url,
            "title": title,
            "description": title,  # Browse API summary doesn't give full desc
            "miles": None,
            "source": SOURCE,
        })
    return out
