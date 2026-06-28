import sys
import os
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

from src.database.db_config import initialize_db
from src.scraper.extractor import MagicBricksScraper
from src.database.crud import upsert_properties

def main():
    logger.info("Starting Real Estate Data Pipeline")
    
    # Step 1: Initialize DB
    logger.info("Initializing Database...")
    initialize_db()
    
    # Step 2: Scrape Data
    cities = ["Dehradun", "Bangalore", "Delhi"]
    scraper = MagicBricksScraper()
    
    for city in cities:
        logger.info(f"Scraping data for {city}...")
        df = scraper.scrape_city(city, limit=30)
        
        if not df.empty:
            logger.info(f"Scraped {len(df)} properties for {city}.")
            # Step 3: Load into DB
            rows = upsert_properties(df)
            logger.info(f"Inserted/Updated {rows} records in the database.")
        else:
            logger.warning(f"No data found for {city}.")
            
    logger.info("Pipeline Execution Completed.")

if __name__ == "__main__":
    main()
