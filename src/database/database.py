import sqlite3
from typing import List, Dict, Any, Optional

class DatabaseLayer:
    def __init__(self, db_name: Optional[str] = None):
        if db_name is None:
            import os
            db_name = os.path.abspath(os.path.join(os.path.dirname(__file__), 'real_estate.db'))
        self.db_name = db_name

    def _get_connection(self):
        conn = sqlite3.connect(self.db_name)
        conn.row_factory = sqlite3.Row
        return conn

    def init_db(self) -> None:
        """1. Database creation script & 5. Index optimization"""
        conn = self._get_connection()
        try:
            cursor = conn.cursor()
            
            # Create locations table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS locations (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    city TEXT NOT NULL,
                    state TEXT NOT NULL,
                    zip_code TEXT,
                    neighborhood TEXT,
                    UNIQUE(city, state, zip_code, neighborhood)
                )
            ''')
            
            # Create properties table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS properties (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    location_id INTEGER,
                    address TEXT NOT NULL,
                    property_type TEXT,
                    bedrooms INTEGER,
                    bathrooms REAL,
                    square_feet REAL,
                    year_built INTEGER,
                    price REAL,
                    listing_date DATE,
                    status TEXT,
                    FOREIGN KEY (location_id) REFERENCES locations (id)
                )
            ''')
            
            # Create market_metrics table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS market_metrics (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    location_id INTEGER,
                    metric_date DATE,
                    median_price REAL,
                    avg_days_on_market REAL,
                    active_listings INTEGER,
                    inventory_months REAL,
                    price_per_sqft REAL,
                    FOREIGN KEY (location_id) REFERENCES locations (id)
                )
            ''')
            
            # 5. Index optimization
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_properties_location ON properties(location_id)')
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_properties_price ON properties(price)')
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_properties_status ON properties(status)')
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_locations_city_state ON locations(city, state)')
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_market_metrics_location_date ON market_metrics(location_id, metric_date)')
            
            conn.commit()
        finally:
            conn.close()

    # 2. Insert functions
    def insert_location(self, city: str, state: str, zip_code: Optional[str] = None, neighborhood: Optional[str] = None) -> int:
        conn = self._get_connection()
        try:
            cursor = conn.cursor()
            try:
                cursor.execute('''
                    INSERT INTO locations (city, state, zip_code, neighborhood)
                    VALUES (?, ?, ?, ?)
                ''', (city, state, zip_code, neighborhood))
                conn.commit()
                return cursor.lastrowid
            except sqlite3.IntegrityError:
                cursor.execute('''
                    SELECT id FROM locations 
                    WHERE city=? AND state=? AND IFNULL(zip_code, '')=? AND IFNULL(neighborhood, '')=?
                ''', (city, state, zip_code or '', neighborhood or ''))
                row = cursor.fetchone()
                return row['id'] if row else -1
        finally:
            conn.close()

    def insert_property(self, location_id: int, address: str, property_type: str, bedrooms: int, bathrooms: float, square_feet: float, year_built: int, price: float, listing_date: str, status: str) -> int:
        conn = self._get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO properties (location_id, address, property_type, bedrooms, bathrooms, square_feet, year_built, price, listing_date, status)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (location_id, address, property_type, bedrooms, bathrooms, square_feet, year_built, price, listing_date, status))
            conn.commit()
            return cursor.lastrowid
        finally:
            conn.close()

    def insert_market_metric(self, location_id: int, metric_date: str, median_price: float, avg_days_on_market: float, active_listings: int, inventory_months: float, price_per_sqft: float) -> int:
        conn = self._get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO market_metrics (location_id, metric_date, median_price, avg_days_on_market, active_listings, inventory_months, price_per_sqft)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (location_id, metric_date, median_price, avg_days_on_market, active_listings, inventory_months, price_per_sqft))
            conn.commit()
            return cursor.lastrowid
        finally:
            conn.close()

    # 3. Update functions
    def update_property(self, property_id: int, **kwargs) -> None:
        if not kwargs:
            return
            
        updates = []
        params = []
        for key, value in kwargs.items():
            updates.append(f"{key} = ?")
            params.append(value)
            
        params.append(property_id)
        
        conn = self._get_connection()
        try:
            cursor = conn.cursor()
            query = f"UPDATE properties SET {', '.join(updates)} WHERE id = ?"
            cursor.execute(query, tuple(params))
            conn.commit()
        finally:
            conn.close()

    def update_market_metric(self, metric_id: int, **kwargs) -> None:
        if not kwargs:
            return
            
        updates = []
        params = []
        for key, value in kwargs.items():
            updates.append(f"{key} = ?")
            params.append(value)
            
        params.append(metric_id)
        
        conn = self._get_connection()
        try:
            cursor = conn.cursor()
            query = f"UPDATE market_metrics SET {', '.join(updates)} WHERE id = ?"
            cursor.execute(query, tuple(params))
            conn.commit()
        finally:
            conn.close()

    # 4. Query functions
    def get_properties_by_location(self, location_id: int, status: Optional[str] = None) -> List[Dict[str, Any]]:
        conn = self._get_connection()
        try:
            cursor = conn.cursor()
            if status:
                cursor.execute("SELECT * FROM properties WHERE location_id = ? AND status = ?", (location_id, status))
            else:
                cursor.execute("SELECT * FROM properties WHERE location_id = ?", (location_id,))
            return [dict(row) for row in cursor.fetchall()]
        finally:
            conn.close()

    def get_market_metrics(self, location_id: int, start_date: Optional[str] = None, end_date: Optional[str] = None) -> List[Dict[str, Any]]:
        conn = self._get_connection()
        try:
            cursor = conn.cursor()
            query = "SELECT * FROM market_metrics WHERE location_id = ?"
            params = [location_id]
            
            if start_date:
                query += " AND metric_date >= ?"
                params.append(start_date)
            if end_date:
                query += " AND metric_date <= ?"
                params.append(end_date)
                
            query += " ORDER BY metric_date ASC"
            cursor.execute(query, tuple(params))
            return [dict(row) for row in cursor.fetchall()]
        finally:
            conn.close()

    def search_properties(self, min_price: Optional[float] = None, max_price: Optional[float] = None, 
                          min_beds: Optional[int] = None, city: Optional[str] = None) -> List[Dict[str, Any]]:
        conn = self._get_connection()
        try:
            cursor = conn.cursor()
            query = '''
                SELECT p.*, l.city, l.state, l.zip_code, l.neighborhood
                FROM properties p
                JOIN locations l ON p.location_id = l.id
                WHERE 1=1
            '''
            params = []
            
            if min_price is not None:
                query += " AND p.price >= ?"
                params.append(min_price)
            if max_price is not None:
                query += " AND p.price <= ?"
                params.append(max_price)
            if min_beds is not None:
                query += " AND p.bedrooms >= ?"
                params.append(min_beds)
            if city is not None:
                query += " AND l.city = ?"
                params.append(city)
                
            cursor.execute(query, tuple(params))
            return [dict(row) for row in cursor.fetchall()]
        finally:
            conn.close()

if __name__ == '__main__':
    db = DatabaseLayer()
    db.init_db()
