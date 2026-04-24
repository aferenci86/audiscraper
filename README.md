# R8 Scraper

Hunts for Audi R8 V8/V10 manual listings under 60k miles across BaT, PCarMarket, eBay, Craigslist, KSL, CarGurus, AutoTrader, and Cars.com. Texts you matches via Twilio. Runs on GitHub Actions, twice weekly.

## One-time setup

### 1. Push to GitHub
Create a repo, drop these files in, push.

### 2. Get accounts
- **Twilio** (twilio.com) — free trial, buy a number (~$1.15/mo). Grab `Account SID`, `Auth Token`, and your Twilio number.
- **eBay Developer** (developer.ebay.com) — free. Create an app, get Client ID + Client Secret. Combine as `CLIENTID:CLIENTSECRET`.

### 3. Add repo secrets
**Settings → Secrets and variables → Actions → New repository secret**

| Name | Value |
|---|---|
| `TWILIO_SID` | from Twilio console |
| `TWILIO_TOKEN` | from Twilio console |
| `TWILIO_FROM` | your Twilio number, e.g. `+15551234567` |
| `TWILIO_TO` | your cell, e.g. `+15557654321` |
| `EBAY_APP_ID` | `clientid:clientsecret` |

### 4. Test
Go to **Actions tab → R8 Scraper → Run workflow**. Check the log:
- Each site prints a raw count
- Filtered count after R8/V8-V10/manual/<60k miles filter
- New-since-last-run count
- Whether Twilio fired

First run will surface every currently-listed matching car as "new" — expect a chunky text.

## Schedule

`scrape.yml` runs cron `0 15 * * 1,4` — Monday and Thursday at 15:00 UTC. Edit the cron line to change. GitHub's cron can be delayed 10-30 minutes; that's normal.

## Tuning

- **Miles cap / keywords / allowed engines** — `config.py`
- **Max listings per SMS** — `MAX_SMS_LISTINGS` in `config.py` (default 8)
- **Craigslist metros** — `CITIES` in `scrapers/craigslist.py`

## Maintenance

HTML scrapers (CarGurus, AutoTrader, Cars.com, KSL, PCarMarket) will break when sites redesign. Symptom: "raw: 0" in the logs for that source across multiple runs. Fix by inspecting a current search page and updating the CSS selectors in that scraper file.

Stable sources (use RSS/API): BaT, eBay, Craigslist. These rarely break.

If CarGurus/AutoTrader/Cars.com start returning 0 from day one, they're blocking GitHub's IP range. Options:
- Drop them (BaT + eBay + CL catch most serious listings anyway)
- Add a proxy via ScraperAPI/Bright Data (~$10-20/mo) — swap `fetch()` in `scrapers/http.py` for the proxied equivalent

## State

`seen.db` (SQLite) stores which listings you've already been texted about. The workflow commits it back to the repo each run so state persists. Don't delete it unless you want a flood of "new" listings next run.

## Local dry run

```bash
pip install -r requirements.txt
python main.py
```

Without Twilio creds set, it'll print to stdout instead of texting.
