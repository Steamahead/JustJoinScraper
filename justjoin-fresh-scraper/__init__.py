import logging, traceback, os, sys

# 1) Sanity-check all imports at module load
try:
    import requests
    from bs4 import BeautifulSoup
    from azure.storage.blob import BlobServiceClient
    import azure.functions as func
    # (add any other imports you need here)

    # 2) Ensure our scraper module is on the path
    root = os.path.abspath(os.path.dirname(__file__))
    if root not in sys.path:
        sys.path.insert(0, root)

    # 3) Import our scraping logic
    from scraper import scrape_justjoin

    logging.info("✅ justjoin-fresh-scraper: Module imports succeeded")

except Exception as e:
    logging.error("🚨 justjoin-fresh-scraper: STARTUP FAILURE: %s", e, exc_info=True)
    raise

def main(timer: func.TimerRequest) -> None:
    logging.info("▶️ justjoin-fresh-scraper: Scrape triggered")
    try:
        jobs = scrape_justjoin()
        logging.info(f"✅ justjoin-fresh-scraper: Scraped {len(jobs)} jobs")
    except Exception as e:
        logging.error("❌ justjoin-fresh-scraper: Runtime error", exc_info=True)
        raise
