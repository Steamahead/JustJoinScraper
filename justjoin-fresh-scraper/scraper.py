import requests
from bs4 import BeautifulSoup
from typing import List, Dict
import logging

API_URL = "https://justjoin.it/api/offers"

def scrape_justjoin() -> List[Dict]:
    """
    Fetch the list of current job offers from JustJoin.it's JSON API.
    """
    logging.info("justjoin-fresh.scraper: Fetching JSON from %s", API_URL)
    resp = requests.get(API_URL, timeout=10)
    resp.raise_for_status()
    data = resp.json()   # this endpoint returns a JSON array of offers :contentReference[oaicite:0]{index=0}
    jobs: List[Dict] = []
    for item in data:
        jobs.append({
            "id": item.get("id"),
            "title": item.get("title"),
            "company": item.get("company_name"),
            "url": f"https://justjoin.it/offers/{item.get('id')}",
            "tags": [t["name"] for t in item.get("tags", [])],
            "posted_at": item.get("published_at"),
        })
    return jobs
