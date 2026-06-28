import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'data', 'real_estate.db')

def get_connection():
    """Returns a connection to the SQLite database."""
    # Ensure directory exists
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    return sqlite3.connect(DB_PATH)

def initialize_db():
    """Initializes the database schema."""
    conn = get_connection()
    cursor = conn.cursor()
    
    # Table for properties
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS properties (
        property_id TEXT PRIMARY KEY,
        property_name TEXT,
        city TEXT,
        locality TEXT,
        property_type TEXT,
        area_sqft REAL,
        price REAL,
        price_per_sqft REAL,
        bedrooms INTEGER,
        bathrooms INTEGER,
        amenities TEXT,
        listing_date DATE,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    ''')
    
    # Index for fast querying by city and locality
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_location ON properties(city, locality)')
    
    conn.commit()
    conn.close()
    print(f"Database initialized at {DB_PATH}")

if __name__ == "__main__":
    initialize_db()
