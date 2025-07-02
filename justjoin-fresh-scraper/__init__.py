import logging, traceback, os, sys

# 1) Check critical imports
try:
    import requests
    from bs4 import BeautifulSoup
    import azure.functions as func
    logging.info("✅ Dependencies imported successfully")
except Exception as e:
    logging.error("🚨 IMPORT ERROR: %s", e, exc_info=True)
    raise

# 2) Ensure scraper.py is on the path
root = os.path.abspath(os.path.dirname(__file__))
if root not in sys.path:
    sys.path.insert(0, root)

# 3) Import your scraper logic
try:
    from scraper import scrape_justjoin
    logging.info("✅ scraper module imported")
except Exception as e:
    logging.error("🚨 SCRAPER IMPORT ERROR: %s", e, exc_info=True)
    raise

def main(timer: func.TimerRequest) -> None:
    logging.info("▶️ justjoin-fresh-scraper: Scrape triggered")
    try:
        jobs = scrape_justjoin()
        logging.info(f"✅ justjoin-fresh-scraper: Scraped {len(jobs)} jobs")
    except Exception as e:
        logging.error("❌ justjoin-fresh-scraper: Error during scrape", exc_info=True)
        raise
