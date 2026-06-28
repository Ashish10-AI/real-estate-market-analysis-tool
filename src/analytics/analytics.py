import pandas as pd
import numpy as np
import sqlite3
from typing import Dict, Any, List, Optional
import os

class AnalyticsEngine:
    def __init__(self, db_path: Optional[str] = None):
        if db_path is None:
            self.db_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'database', 'real_estate.db'))
        else:
            self.db_path = db_path

    def _get_connection(self) -> sqlite3.Connection:
        """Establish and return a database connection."""
        return sqlite3.connect(self.db_path)

    def load_properties_data(self) -> pd.DataFrame:
        """Load properties and locations into a single DataFrame."""
        query = '''
            SELECT p.*, l.city, l.state, l.zip_code, l.neighborhood
            FROM properties p
            JOIN locations l ON p.location_id = l.id
        '''
        with self._get_connection() as conn:
            df = pd.read_sql_query(query, conn)
            
        if not df.empty:
            df['listing_date'] = pd.to_datetime(df['listing_date'])
            df['price_per_sqft'] = df['price'] / df['square_feet'].replace(0, np.nan)
        return df
        
    def load_market_metrics(self) -> pd.DataFrame:
        """Load market metrics and locations into a single DataFrame."""
        query = '''
            SELECT m.*, l.city, l.state, l.neighborhood
            FROM market_metrics m
            JOIN locations l ON m.location_id = l.id
        '''
        with self._get_connection() as conn:
            df = pd.read_sql_query(query, conn)
        
        if not df.empty:
            df['metric_date'] = pd.to_datetime(df['metric_date'])
        return df

    # --- Basic Metrics ---

    def average_property_price(self, df: pd.DataFrame) -> float:
        """1. Average Property Price"""
        if df.empty or 'price' not in df.columns:
            return 0.0
        return float(df['price'].mean())

    def median_property_price(self, df: pd.DataFrame) -> float:
        """2. Median Property Price"""
        if df.empty or 'price' not in df.columns:
            return 0.0
        return float(df['price'].median())

    def price_per_sqft_distribution(self, df: pd.DataFrame) -> Dict[str, float]:
        """3. Price Per Sqft Distribution"""
        if df.empty or 'price_per_sqft' not in df.columns:
            return {}
        return df['price_per_sqft'].dropna().describe().to_dict()

    def top_localities(self, df: pd.DataFrame, top_n: int = 5) -> pd.DataFrame:
        """4. Top Localities (Based on listing volume)"""
        if df.empty or 'neighborhood' not in df.columns:
            return pd.DataFrame()
        return df['neighborhood'].value_counts().head(top_n).reset_index().rename(
            columns={'neighborhood': 'neighborhood', 'count': 'listing_count'}
        )

    def cheapest_areas(self, df: pd.DataFrame, top_n: int = 5) -> pd.DataFrame:
        """5. Cheapest Areas (Based on median price)"""
        if df.empty or 'neighborhood' not in df.columns or 'price' not in df.columns:
            return pd.DataFrame()
        return df.groupby('neighborhood')['price'].median().nsmallest(top_n).reset_index(name='median_price')

    def premium_areas(self, df: pd.DataFrame, top_n: int = 5) -> pd.DataFrame:
        """6. Premium Areas (Based on median price)"""
        if df.empty or 'neighborhood' not in df.columns or 'price' not in df.columns:
            return pd.DataFrame()
        return df.groupby('neighborhood')['price'].median().nlargest(top_n).reset_index(name='median_price')

    def price_trend_analysis(self, df: pd.DataFrame) -> pd.DataFrame:
        """7. Price Trend Analysis (Monthly average price)"""
        if df.empty or 'listing_date' not in df.columns or 'price' not in df.columns:
            return pd.DataFrame()
        # Group by year-month
        trend_df = df.copy()
        trend_df['month_year'] = trend_df['listing_date'].dt.to_period('M')
        return trend_df.groupby('month_year')['price'].mean().reset_index(name='avg_price')

    def property_type_analysis(self, df: pd.DataFrame) -> pd.DataFrame:
        """8. Property Type Analysis"""
        if df.empty or 'property_type' not in df.columns:
            return pd.DataFrame()
        return df.groupby('property_type').agg(
            avg_price=('price', 'mean'),
            median_price=('price', 'median'),
            count=('id', 'count')
        ).reset_index()

    def investment_opportunity_score(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        9. Investment Opportunity Score
        Scores properties based on price per sqft vs neighborhood average, and age of property.
        """
        if df.empty or 'price_per_sqft' not in df.columns or 'year_built' not in df.columns:
            return pd.DataFrame()
        
        # Calculate neighborhood avg price per sqft
        nb_avg = df.groupby('neighborhood')['price_per_sqft'].transform('mean')
        
        # Calculate factors (handle divisions by zero/NaN)
        price_factor = np.where(nb_avg > 0, (nb_avg - df['price_per_sqft']) / nb_avg, 0)
        
        min_year = df['year_built'].min()
        max_year = df['year_built'].max()
        if max_year > min_year:
            age_factor = (df['year_built'] - min_year) / (max_year - min_year)
        else:
            age_factor = 0.5 # Default if all properties are same age
            
        df['investment_score'] = (price_factor * 0.7) + (age_factor * 0.3)
        
        # Normalize to 0-100
        min_score = df['investment_score'].min()
        max_score = df['investment_score'].max()
        if max_score > min_score:
            df['investment_score'] = ((df['investment_score'] - min_score) / (max_score - min_score)) * 100
        else:
            df['investment_score'] = 50.0
                                  
        return df[['id', 'address', 'neighborhood', 'price', 'investment_score']].sort_values(by='investment_score', ascending=False)

    # --- Advanced Analytics ---

    def undervalued_property_detection(self, df: pd.DataFrame, threshold_percent: float = 0.15) -> pd.DataFrame:
        """10. Undervalued Property Detection"""
        if df.empty or 'price' not in df.columns or 'neighborhood' not in df.columns:
            return pd.DataFrame()
        
        nb_median = df.groupby('neighborhood')['price'].transform('median')
        df['undervalued_margin'] = np.where(nb_median > 0, (nb_median - df['price']) / nb_median, 0)
        
        undervalued = df[df['undervalued_margin'] >= threshold_percent]
        return undervalued[['id', 'address', 'neighborhood', 'price', 'undervalued_margin']].sort_values(by='undervalued_margin', ascending=False)

    def high_growth_locality_detection(self, metrics_df: pd.DataFrame) -> pd.DataFrame:
        """11. High Growth Locality Detection"""
        if metrics_df.empty or 'median_price' not in metrics_df.columns:
            return pd.DataFrame()
        
        # Ensure correct temporal order
        metrics_df = metrics_df.sort_values(by=['neighborhood', 'metric_date'])
        
        # Calculate period-over-period price growth per neighborhood
        metrics_df['price_growth'] = metrics_df.groupby('neighborhood')['median_price'].pct_change()
        
        # Average growth over all periods
        growth = metrics_df.groupby('neighborhood')['price_growth'].mean().reset_index()
        growth = growth.dropna()
        return growth.sort_values(by='price_growth', ascending=False)

    def affordability_index(self, df: pd.DataFrame, median_income: float = 75000) -> pd.DataFrame:
        """
        12. Affordability Index
        (Median Income / Median Property Price) * 100
        """
        if df.empty or 'price' not in df.columns:
            return pd.DataFrame()
            
        affordability = df.groupby('neighborhood').agg(
            median_price=('price', 'median')
        ).reset_index()
        
        affordability['affordability_index'] = np.where(
            affordability['median_price'] > 0, 
            (median_income / affordability['median_price']) * 100, 
            0
        )
        return affordability.sort_values(by='affordability_index', ascending=False)

    def market_demand_index(self, metrics_df: pd.DataFrame) -> pd.DataFrame:
        """
        13. Market Demand Index
        Based on active listings and days on market (lower is better for demand).
        """
        if metrics_df.empty or 'avg_days_on_market' not in metrics_df.columns or 'inventory_months' not in metrics_df.columns:
            return pd.DataFrame()
            
        latest_metrics = metrics_df.sort_values('metric_date').groupby('neighborhood').last().reset_index()
        
        max_dom = latest_metrics['avg_days_on_market'].max()
        max_inv = latest_metrics['inventory_months'].max()
        
        # Safe division
        dom_score = 1 - (latest_metrics['avg_days_on_market'] / max_dom) if max_dom > 0 else 0
        inv_score = 1 - (latest_metrics['inventory_months'] / max_inv) if max_inv > 0 else 0
        
        latest_metrics['demand_index'] = (dom_score * 0.6 + inv_score * 0.4) * 100
        
        return latest_metrics[['neighborhood', 'demand_index']].sort_values(by='demand_index', ascending=False)

if __name__ == '__main__':
    # Initialize engine
    engine = AnalyticsEngine()
    print("Analytics Engine initialized. Connect to a populated database to test methods.")
