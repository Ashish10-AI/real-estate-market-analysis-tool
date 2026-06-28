import pandas as pd
from src.database.crud import get_all_properties

def get_market_overview():
    """Returns top-level KPIs for the dashboard."""
    df = get_all_properties()
    if df.empty:
        return {}
    
    return {
        'total_listings': len(df),
        'avg_price': df['price'].mean(),
        'avg_price_sqft': df['price_per_sqft'].mean(),
        'cities': df['city'].nunique(),
        'localities': df['locality'].nunique()
    }

def get_price_by_locality():
    """Aggregates average price and price per sqft by locality."""
    df = get_all_properties()
    if df.empty:
        return pd.DataFrame()
        
    locality_stats = df.groupby(['city', 'locality']).agg(
        avg_price=('price', 'mean'),
        avg_price_sqft=('price_per_sqft', 'mean'),
        listing_count=('property_id', 'count')
    ).reset_index()
    
    return locality_stats.sort_values(by='avg_price', ascending=False)

def find_investment_opportunities(discount_threshold=0.15):
    """
    Identifies properties priced significantly below the locality average.
    discount_threshold: e.g., 0.15 means 15% below average.
    """
    df = get_all_properties()
    if df.empty:
        return pd.DataFrame()
        
    locality_avg = df.groupby('locality')['price_per_sqft'].mean().reset_index()
    locality_avg.rename(columns={'price_per_sqft': 'locality_avg_sqft'}, inplace=True)
    
    merged = pd.merge(df, locality_avg, on='locality', how='left')
    
    # Calculate discount
    merged['discount_pct'] = (merged['locality_avg_sqft'] - merged['price_per_sqft']) / merged['locality_avg_sqft']
    
    # Filter properties
    opportunities = merged[merged['discount_pct'] >= discount_threshold].copy()
    opportunities.sort_values(by='discount_pct', ascending=False, inplace=True)
    
    return opportunities
    
def get_amenity_impact():
    """Calculates average price based on presence of key amenities."""
    df = get_all_properties()
    if df.empty:
        return pd.DataFrame()
        
    # Extremely simplified amenity extraction
    amenities_list = ['Gym', 'Pool', 'Security', 'Parking']
    
    results = []
    for amenity in amenities_list:
        has_amenity = df[df['amenities'].str.contains(amenity, case=False, na=False)]
        no_amenity = df[~df['amenities'].str.contains(amenity, case=False, na=False)]
        
        avg_with = has_amenity['price'].mean() if not has_amenity.empty else 0
        avg_without = no_amenity['price'].mean() if not no_amenity.empty else 0
        
        premium = ((avg_with - avg_without) / avg_without) * 100 if avg_without > 0 else 0
        
        results.append({
            'amenity': amenity,
            'avg_price_with': avg_with,
            'avg_price_without': avg_without,
            'premium_pct': premium
        })
        
    return pd.DataFrame(results)
