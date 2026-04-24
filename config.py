"""Central config. All tunables live here."""
import os

# ---- Filter criteria ----
MAX_MILES = 60_000
REQUIRED_KEYWORDS_ANY = ["r8"]  # must contain at least one
# Engine / transmission filters applied on top of "r8":
REQUIRE_MANUAL_TRANSMISSION = True
ALLOWED_ENGINES = ["v8", "v10"]  # at least one must match

# Words that strongly suggest NOT-manual, used to reject false positives
AUTO_TRANS_NEGATIVES = [
    "r-tronic", "r tronic", "rtronic",
    "s-tronic", "s tronic", "stronic",
    "automatic", "auto trans", "tiptronic", "dct", "dual clutch",
    "paddle shift only", "paddle-shift only",
]

MANUAL_POSITIVES = [
    "6-speed manual", "6 speed manual", "6mt", "manual transmission",
    "gated manual", "stick shift", "three-pedal", "three pedal", "3-pedal",
    "manual gearbox", "6-spd manual", "6spd manual",
]

# ---- Secrets from env (GitHub Actions secrets) ----
TWILIO_SID = os.environ.get("TWILIO_SID", "")
TWILIO_TOKEN = os.environ.get("TWILIO_TOKEN", "")
TWILIO_FROM = os.environ.get("TWILIO_FROM", "")  # your Twilio number
TWILIO_TO = os.environ.get("TWILIO_TO", "")      # your cell number

EBAY_APP_ID = os.environ.get("EBAY_APP_ID", "")  # eBay Browse API

# ---- Behavior ----
DB_PATH = os.environ.get("DB_PATH", "seen.db")
USER_AGENT = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
    "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36"
)
REQUEST_TIMEOUT = 20
MAX_SMS_LISTINGS = 8  # cap per run so you don't get a novel via text
