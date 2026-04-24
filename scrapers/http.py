"""Shared HTTP session with sane defaults."""
import requests
from config import USER_AGENT, REQUEST_TIMEOUT


def get_session():
    s = requests.Session()
    s.headers.update({
        "User-Agent": USER_AGENT,
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.9",
    })
    return s


def fetch(url: str, session=None, **kwargs):
    s = session or get_session()
    kwargs.setdefault("timeout", REQUEST_TIMEOUT)
    r = s.get(url, **kwargs)
    r.raise_for_status()
    return r
