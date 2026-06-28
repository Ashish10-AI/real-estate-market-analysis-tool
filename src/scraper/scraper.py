import time
import random
import logging
from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def retry(max_attempts=3, delay_secs=2, backoff_factor=2):
    """Decorator to implement exponential backoff retry logic."""
    def decorator(func):
        def wrapper(*args, **kwargs):
            attempts = 0
            current_delay = delay_secs
            while attempts < max_attempts:
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    attempts += 1
                    logger.warning(f"Attempt {attempts}/{max_attempts} failed for {func.__name__}: {str(e)}")
                    if attempts >= max_attempts:
                        logger.error(f"Function {func.__name__} failed after {max_attempts} attempts.")
                        raise
                    time.sleep(current_delay)
                    current_delay *= backoff_factor
        return wrapper
    return decorator

class BaseScraper:
    def __init__(self, base_url: str):
        self.base_url = base_url
        # Simulate setting up a robust requests.Session with headers
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5'
        }

    @retry(max_attempts=3)
    def fetch_page(self, endpoint: str) -> str:
        """Simulate fetching a webpage securely."""
        # In a purely live scraper, this would be:
        # response = requests.get(f"{self.base_url}{endpoint}", headers=self.headers)
        # response.raise_for_status()
        # return response.text
        
        # Simulate network delay to mimic real scraping
        time.sleep(random.uniform(0.1, 0.4))
        
        # 10% chance to simulate a network error / IP block to test retry logic
        if random.random() < 0.1:  
            raise ConnectionError("Simulated network timeout/connection reset by peer")
            
        return "<html>Simulated HTML Content</html>"

class MockRealEstateScraper(BaseScraper):
    def __init__(self):
        super().__init__(base_url="https://mock-realestate-site.com")
        self.cities = [
            {"city": "Austin", "state": "TX", "base_price": 600000},
            {"city": "Seattle", "state": "WA", "base_price": 850000},
            {"city": "New York", "state": "NY", "base_price": 1500000},
            {"city": "Denver", "state": "CO", "base_price": 650000},
            {"city": "Miami", "state": "FL", "base_price": 700000},
            {"city": "Chicago", "state": "IL", "base_price": 450000}
        ]
        self.property_types = ["Single Family", "Condo", "Townhouse", "Multi-Family"]
        self.statuses = ["Active", "Pending", "Sold"]

    def _generate_mock_neighborhoods(self, city: str) -> List[str]:
        neighborhoods = {
            "Austin": ["Downtown", "Zilker", "Domain", "Barton Hills", "East Austin"],
            "Seattle": ["Capitol Hill", "Ballard", "Queen Anne", "Fremont", "Belltown"],
            "New York": ["Manhattan", "Brooklyn", "Queens", "Staten Island", "Bronx"],
            "Denver": ["LoDo", "Highlands", "Cherry Creek", "Capitol Hill", "RiNo"],
            "Miami": ["Brickell", "South Beach", "Coral Gables", "Wynwood", "Downtown"],
            "Chicago": ["Lincoln Park", "Wicker Park", "Loop", "River North", "Hyde Park"]
        }
        return neighborhoods.get(city, ["Central"])

    @retry(max_attempts=3)
    def scrape_properties(self, num_properties: int = 500) -> List[Dict[str, Any]]:
        """Scrape (generate) properties with robust error handling and mimicking."""
        logger.info(f"Starting scraping process for {num_properties} properties...")
        properties = []
        
        # Simulate initial search page load
        self.fetch_page("/search")
        
        for i in range(num_properties):
            try:
                # Simulate pagination fetch every 20 properties
                if i > 0 and i % 20 == 0:
                    self.fetch_page(f"/search?page={i//20}")
                    
                city_data = random.choice(self.cities)
                neighborhood = random.choice(self._generate_mock_neighborhoods(city_data["city"]))
                
                prop_type = random.choice(self.property_types)
                bedrooms = random.randint(1, 6)
                bathrooms = bedrooms + random.choice([0, 0.5, 1.0]) if bedrooms > 1 else 1.0
                
                # Base area
                sqft = random.randint(600, 5000)
                
                # Calculate realistic price based on city base and sqft
                price_multiplier = random.uniform(0.7, 1.8)
                price = (city_data["base_price"] * price_multiplier) * (sqft / 2000.0)
                
                # Modifiers
                if prop_type == "Condo":
                    price *= 0.85
                    sqft = random.randint(500, 2000)
                elif prop_type == "Single Family":
                    price *= 1.1
                    sqft = random.randint(1200, 5000)
                    
                listing_date = datetime.now() - timedelta(days=random.randint(1, 120))
                street_names = ["Oak", "Maple", "Pine", "Cedar", "Washington", "Main", "Park", "Lake"]
                street_types = ["St", "Ave", "Blvd", "Ln", "Dr", "Ct"]
                
                properties.append({
                    "city": city_data["city"],
                    "state": city_data["state"],
                    "zip_code": str(random.randint(10000, 99999)),
                    "neighborhood": neighborhood,
                    "address": f"{random.randint(100, 9999)} {random.choice(street_names)} {random.choice(street_types)}",
                    "property_type": prop_type,
                    "bedrooms": bedrooms,
                    "bathrooms": float(bathrooms),
                    "square_feet": float(sqft),
                    "year_built": random.randint(1920, 2023),
                    "price": round(price, 2),
                    "listing_date": listing_date.strftime("%Y-%m-%d"),
                    "status": random.choice(self.statuses)
                })
            except Exception as e:
                logger.error(f"Error parsing property {i}: {str(e)}. Skipping.")
                continue
                
        logger.info(f"Successfully scraped {len(properties)} properties.")
        return properties
