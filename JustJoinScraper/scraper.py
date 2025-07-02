import requests
import logging
from typing import List, Dict

def scrape_justjoin() -> List[Dict]:
    """Fetch job offers from JustJoin.it API"""
    API_URL = "https://justjoin.it/api/offers"
    
    logging.info(f"🔄 Fetching data from: {API_URL}")
    response = requests.get(API_URL, timeout=30)
    response.raise_for_status()
    
    data = response.json()
    jobs = []
    
    for item in data:
        job = {
            "id": item.get("id"),
            "title": item.get("title"),
            "company": item.get("company_name"),
            "url": f"https://justjoin.it/offers/{item.get('id')}",
            "location": item.get("city"),
            "remote": item.get("remote"),
            "published_at": item.get("published_at")
        }
        jobs.append(job)
    
    logging.info(f"✅ Successfully scraped {len(jobs)} jobs")
    return jobs
