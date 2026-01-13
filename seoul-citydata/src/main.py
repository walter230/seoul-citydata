import schedule
import time
import logging
from src.api_client import CityDataAPIClient
from src.db_client import DBClient
from src.config import Config

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("seoul_citydata.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

def job():
    """Main job to fetch and save data"""
    logger.info("Starting data collection job...")
    
    try:
        # Initialize clients
        api_client = CityDataAPIClient()
        db_client = DBClient()
        
        # Fetch data
        logger.info("Fetching data from Seoul API...")
        data_map = api_client.get_data_for_all_targets()
        
        if not data_map:
            logger.warning("No data fetched in this run.")
            return

        # Save data
        logger.info(f"Transforming and saving data for {len(data_map)} areas...")
        db_client.process_and_save(data_map)
        
        logger.info("Job completed successfully.")
        
    except Exception as e:
        logger.error(f"Job failed with error: {e}")

def main():
    """Main entry point"""
    logger.info("Seoul City Data Collector Service Started")
    
    # Run once immediately for verification
    job()
    
    # Schedule job (e.g., every 10 minutes)
    schedule.every(10).minutes.do(job)
    
    logger.info("Scheduler is running. Press Ctrl+C to exit.")
    
    try:
        while True:
            schedule.run_pending()
            time.sleep(1)
    except KeyboardInterrupt:
        logger.info("Service stopped by user.")

if __name__ == "__main__":
    main()
