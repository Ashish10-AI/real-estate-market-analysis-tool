import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os
import sys

# Add parent directory to path to import analytics
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from analytics.analytics import AnalyticsEngine

st.set_page_config(page_title="Real Estate Market Intelligence", layout="wide", initial_sidebar_state="expanded")

@st.cache_data
def get_data():
    db_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'database', 'real_estate.db'))
    engine = AnalyticsEngine(db_path=db_path)
    return engine.load_properties_data()

def main():
    st.title("🏙️ Real Estate Market Intelligence Dashboard")
    st.markdown("Advanced analytics for recruiters and real estate professionals.")

    # Load data
    df = get_data()
    db_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'database', 'real_estate.db'))
    engine = AnalyticsEngine(db_path=db_path)

    if df.empty:
        st.warning("No data found in the database. Please run the scraper or populate the database first.")
        return

    # --- Sidebar Filters ---
    st.sidebar.header("🔍 Filters")
    
    # City Filter
    cities_available = df['city'].dropna().unique()
    cities = st.sidebar.multiselect("City", options=cities_available)
    
    # Locality Filter based on selected cities
    if cities:
        localities_available = df[df['city'].isin(cities)]['neighborhood'].dropna().unique()
    else:
        localities_available = df['neighborhood'].dropna().unique()
    localities = st.sidebar.multiselect("Locality", options=localities_available)
    
    # Property Type Filter
    prop_types_available = df['property_type'].dropna().unique()
    prop_types = st.sidebar.multiselect("Property Type", options=prop_types_available)
    
    # Price Range Filter
    min_price = float(df['price'].min()) if not df['price'].isna().all() else 0.0
    max_price = float(df['price'].max()) if not df['price'].isna().all() else 0.0
    if min_price < max_price:
        price_range = st.sidebar.slider("Price Range ($)", min_value=min_price, max_value=max_price, value=(min_price, max_price))
    else:
        price_range = (min_price, max_price)
        
    # Area Range Filter
    min_area = float(df['square_feet'].min()) if not df['square_feet'].isna().all() else 0.0
    max_area = float(df['square_feet'].max()) if not df['square_feet'].isna().all() else 0.0
    if min_area < max_area:
        area_range = st.sidebar.slider("Area Range (Sqft)", min_value=min_area, max_value=max_area, value=(min_area, max_area))
    else:
        area_range = (min_area, max_area)

    # --- Apply Filters ---
    filtered_df = df.copy()
    if cities:
        filtered_df = filtered_df[filtered_df['city'].isin(cities)]
    if localities:
        filtered_df = filtered_df[filtered_df['neighborhood'].isin(localities)]
    if prop_types:
        filtered_df = filtered_df[filtered_df['property_type'].isin(prop_types)]
        
    filtered_df = filtered_df[(filtered_df['price'] >= price_range[0]) & (filtered_df['price'] <= price_range[1])]
    filtered_df = filtered_df[(filtered_df['square_feet'] >= area_range[0]) & (filtered_df['square_feet'] <= area_range[1])]

    if filtered_df.empty:
        st.info("No properties match the selected filters.")
        return

    # --- KPIs ---
    total_listings = len(filtered_df)
    avg_price = engine.average_property_price(filtered_df)
    median_price = engine.median_property_price(filtered_df)
    avg_price_sqft = filtered_df['price_per_sqft'].mean()

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Listings", f"{total_listings:,}")
    col2.metric("Average Price", f"${avg_price:,.0f}")
    col3.metric("Median Price", f"${median_price:,.0f}")
    col4.metric("Avg Price/Sqft", f"${avg_price_sqft:,.2f}" if pd.notna(avg_price_sqft) else "N/A")

    st.markdown("---")

    # --- Charts ---
    
    # Row 1
    c1, c2 = st.columns(2)
    
    with c1:
        # 1. Price Trend Chart
        trend_df = engine.price_trend_analysis(filtered_df)
        if not trend_df.empty:
            trend_df['month_year'] = trend_df['month_year'].astype(str)
            fig_trend = px.line(trend_df, x='month_year', y='avg_price', markers=True,
                                title="Price Trend Analysis", labels={'month_year': 'Month', 'avg_price': 'Average Price ($)'})
            st.plotly_chart(fig_trend, use_container_width=True)
        else:
            st.info("Not enough temporal data for Price Trend Analysis.")

    with c2:
        # 2. Price Distribution Histogram
        fig_hist = px.histogram(filtered_df, x='price', nbins=50, 
                                title="Price Distribution", labels={'price': 'Price ($)'},
                                color_discrete_sequence=['#3366CC'])
        st.plotly_chart(fig_hist, use_container_width=True)

    # Row 2
    c3, c4 = st.columns(2)
    
    with c3:
        # 3. Top Localities Chart
        top_loc_df = engine.top_localities(filtered_df, top_n=10)
        if not top_loc_df.empty:
            fig_top_loc = px.bar(top_loc_df, x='neighborhood', y='listing_count', 
                                 title="Top Localities by Listings", 
                                 labels={'neighborhood': 'Locality', 'listing_count': 'Listings'},
                                 color='listing_count', color_continuous_scale='Blues')
            st.plotly_chart(fig_top_loc, use_container_width=True)

    with c4:
        # 4. Property Type Breakdown
        prop_type_df = engine.property_type_analysis(filtered_df)
        if not prop_type_df.empty:
            fig_prop = px.pie(prop_type_df, names='property_type', values='count', 
                              title="Property Type Breakdown", hole=0.4)
            fig_prop.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(fig_prop, use_container_width=True)

    # Row 3
    # 5. Heatmap of Price Per Sqft (Using Treemap to represent localities)
    st.subheader("Locality Price Per Sqft Heatmap")
    heatmap_df = filtered_df.dropna(subset=['city', 'neighborhood', 'price_per_sqft'])
    if not heatmap_df.empty:
        # Aggregate to avoid plotting every single property in treemap if it gets too large, 
        # or just plot localities.
        agg_heatmap = heatmap_df.groupby(['city', 'neighborhood']).agg(
            avg_price_sqft=('price_per_sqft', 'mean'),
            count=('id', 'count')
        ).reset_index()
        
        fig_heat = px.treemap(agg_heatmap, path=[px.Constant("All Localities"), 'city', 'neighborhood'], 
                              values='count',
                              color='avg_price_sqft', color_continuous_scale='RdYlGn_r',
                              title="Heatmap: Average Price Per Sqft by Locality (Size = Listings)",
                              labels={'avg_price_sqft': 'Avg Price/Sqft ($)'})
        st.plotly_chart(fig_heat, use_container_width=True)
    else:
        st.info("Not enough data to generate Price Per Sqft Heatmap.")

    st.markdown("---")

    # --- Advanced Features ---
    c5, c6 = st.columns(2)
    
    with c5:
        # 6. Investment Opportunity Rankings
        st.subheader("Top Investment Opportunities")
        inv_df = engine.investment_opportunity_score(filtered_df)
        if not inv_df.empty:
            st.dataframe(inv_df.head(10).style.format({
                'price': '${:,.2f}',
                'investment_score': '{:.1f}/100'
            }), use_container_width=True)
            
    with c6:
        # Search Comparable Properties
        st.subheader("Find Comparable Properties")
        valid_addresses = filtered_df['address'].dropna().unique()
        selected_address = st.selectbox("Select a property to find comparables", options=valid_addresses)
        
        if selected_address:
            prop = filtered_df[filtered_df['address'] == selected_address].iloc[0]
            
            # Simple comparable logic: Same neighborhood, Price +/- 20%, Area +/- 20%
            comps = df[
                (df['neighborhood'] == prop['neighborhood']) &
                (df['address'] != prop['address']) &
                (df['price'] >= prop['price'] * 0.8) &
                (df['price'] <= prop['price'] * 1.2) &
                (df['square_feet'] >= prop['square_feet'] * 0.8) &
                (df['square_feet'] <= prop['square_feet'] * 1.2)
            ]
            
            st.write(f"Found **{len(comps)}** comparable properties in **{prop['neighborhood']}**:")
            if not comps.empty:
                st.dataframe(comps[['address', 'price', 'bedrooms', 'bathrooms', 'square_feet']].style.format({
                    'price': '${:,.0f}'
                }), use_container_width=True)
            else:
                st.info("No comparable properties found based on +/- 20% price and area in the same neighborhood.")

    # Download Data
    st.markdown("---")
    st.subheader("Export Data")
    csv = filtered_df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Download Filtered Data as CSV",
        data=csv,
        file_name='filtered_real_estate_data.csv',
        mime='text/csv',
    )

if __name__ == "__main__":
    main()
