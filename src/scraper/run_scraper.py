import sys
import os
import logging
from datetime import datetime
import pandas as pd
import random

# Add parent directory to path to import modules
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from database.database import DatabaseLayer
from scraper import MockRealEstateScraper
from analytics.analytics import AnalyticsEngine

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def main():
    logger.info("Initializing Real Estate Market Analysis Scraper...")
    
    # Initialize DB
    db = DatabaseLayer()
    db.init_db()
    
    # Initialize Scraper
    scraper = MockRealEstateScraper()
    
    # Scrape data
    num_to_scrape = 500
    properties = scraper.scrape_properties(num_properties=num_to_scrape)
    
    if not properties:
        logger.error("No properties scraped. Exiting.")
        return
        
    logger.info("Inserting scraped data into database...")
    
    # Insert Locations and Properties
    properties_inserted = 0
    
    for prop in properties:
        loc_id = db.insert_location(
            city=prop['city'],
            state=prop['state'],
            zip_code=prop['zip_code'],
            neighborhood=prop['neighborhood']
        )
        
        if loc_id != -1:
            db.insert_property(
                location_id=loc_id,
                address=prop['address'],
                property_type=prop['property_type'],
                bedrooms=prop['bedrooms'],
                bathrooms=prop['bathrooms'],
                square_feet=prop['square_feet'],
                year_built=prop['year_built'],
                price=prop['price'],
                listing_date=prop['listing_date'],
                status=prop['status']
            )
            properties_inserted += 1
            
    logger.info(f"Database populated with {properties_inserted} new properties.")
    
    logger.info("Generating market metrics from new data...")
    # Generate market metrics based on inserted data
    engine = AnalyticsEngine()
    all_props = engine.load_properties_data()
    
    if not all_props.empty:
        current_date = datetime.now().strftime('%Y-%m-%d')
        grouped = all_props.groupby(['city', 'state', 'neighborhood'])
        metrics_count = 0
        
        for name, group in grouped:
            city, state, neighborhood = name
            
            # Retrieve or insert location to get its ID
            loc_id = db.insert_location(city, state, neighborhood=neighborhood)
            
            median_price = group['price'].median()
            active_listings = len(group[group['status'] == 'Active'])
            avg_dom = random.randint(10, 75) # Simulated days on market
            inventory_months = random.uniform(0.5, 8.0) # Simulated inventory
            price_per_sqft = group['price_per_sqft'].mean()
            
            db.insert_market_metric(
                location_id=loc_id,
                metric_date=current_date,
                median_price=float(median_price),
                avg_days_on_market=float(avg_dom),
                active_listings=active_listings,
                inventory_months=float(inventory_months),
                price_per_sqft=float(price_per_sqft)
            )
            metrics_count += 1
            
        logger.info(f"Generated and inserted {metrics_count} market metrics.")
        
    logger.info("Scraping pipeline completed successfully!")

if __name__ == "__main__":
    main()
