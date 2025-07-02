import logging
import json
import azure.functions as func
from .scraper import scrape_justjoin  # Import from separate file

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('🚀 HTTP trigger function processed a request.')

    try:
        jobs = scrape_justjoin()
        
        return func.HttpResponse(
            json.dumps({
                "status": "success",
                "jobs_count": len(jobs),
                "sample_jobs": jobs[:3]  # Return first 3 jobs as sample
            }),
            status_code=200,
            mimetype="application/json"
        )
        
    except Exception as e:
        logging.error(f"❌ Error: {str(e)}")
        return func.HttpResponse(
            json.dumps({
                "status": "error",
                "message": str(e)
            }),
            status_code=500,
            mimetype="application/json"
        )
