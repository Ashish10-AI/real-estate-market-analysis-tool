import sqlite3
import pandas as pd
from .db_config import get_connection

def upsert_properties(df):
    """
    Inserts new properties or updates existing ones based on property_id.
    Takes a pandas DataFrame as input.
    """
    if df.empty:
        return 0

    conn = get_connection()
    cursor = conn.cursor()
    
    upsert_sql = '''
    INSERT INTO properties (
        property_id, property_name, city, locality, property_type, 
        area_sqft, price, price_per_sqft, bedrooms, bathrooms, 
        amenities, listing_date
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ON CONFLICT(property_id) DO UPDATE SET
        price=excluded.price,
        price_per_sqft=excluded.price_per_sqft,
        listing_date=excluded.listing_date
    '''
    
    # Fill NaN values with None for SQLite
    df = df.where(pd.notnull(df), None)
    
    records = df[[
        'property_id', 'property_name', 'city', 'locality', 'property_type',
        'area_sqft', 'price', 'price_per_sqft', 'bedrooms', 'bathrooms',
        'amenities', 'listing_date'
    ]].values.tolist()
    
    cursor.executemany(upsert_sql, records)
    conn.commit()
    rows_affected = cursor.rowcount
    conn.close()
    return rows_affected

def get_all_properties():
    """Returns all properties as a pandas DataFrame."""
    conn = get_connection()
    df = pd.read_sql_query("SELECT * FROM properties", conn)
    conn.close()
    return df
