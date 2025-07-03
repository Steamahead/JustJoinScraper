import logging
import traceback
import requests
import azure.functions as func
from typing import List, Dict

def scrape_justjoin() -> List[Dict]:
    """Fetch job offers from JustJoin.it API"""
    API_URL = "https://justjoin.it/api/offers"
    
    try:
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
                "employment_types": item.get("employment_types", []),
                "experience_level": item.get("experience_level"),
                "tags": [tag.get("name") for tag in item.get("marker_icon", [])],
                "published_at": item.get("published_at"),
                "salary": item.get("employment_types", [{}])[0].get("salary") if item.get("employment_types") else None
            }
            jobs.append(job)
        
        logging.info(f"✅ Successfully scraped {len(jobs)} jobs")
        return jobs
        
    except requests.exceptions.Timeout:
        logging.error("⏱️ Request timeout")
        raise
    except requests.exceptions.RequestException as e:
        logging.error(f"🌐 Request error: {e}")
        raise
    except Exception as e:
        logging.error(f"💥 Unexpected error: {e}")
        raise

def main(timer: func.TimerRequest) -> None:
    """Main Azure Function entry point"""
    
    if timer.past_due:
        logging.info('⚠️ Timer is past due!')

    logging.info('🚀 JustJoinScraper function started')
    
    try:
        jobs = scrape_justjoin()
        
        # Log some sample data
        if jobs:
            sample_job = jobs[0]
            logging.info(f"📋 Sample job: {sample_job.get('title')} at {sample_job.get('company')}")
        
        logging.info(f"✅ Function completed successfully. Found {len(jobs)} jobs")
        
    except Exception as e:
        logging.error(f"❌ Function failed: {str(e)}")
        logging.error(f"🔍 Traceback: {traceback.format_exc()}")
        raise
