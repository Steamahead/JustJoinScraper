import logging
import azure.functions as func

from scraper import scrape_justjoin

def main(timer: func.TimerRequest) -> None:
    logging.info("▶️ justjoin-fresh: Scrape triggered")
    try:
        jobs = scrape_justjoin()
        logging.info(f"✅ justjoin-fresh: Scraped {len(jobs)} jobs")
    except Exception as e:
        logging.error("❌ justjoin-fresh: Error scraping JustJoin", exc_info=True)
        raise
