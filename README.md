# Real Estate Market Intelligence Platform

A portfolio-grade data pipeline and Streamlit dashboard that collects property listings from MagicBricks, stores them in SQLite, performs market analysis, and identifies investment opportunities.

## Features
- **Automated Web Scraper**: Extracts listings for Dehradun, Bangalore, and Delhi/NCR.
- **Data Warehouse**: Stores historical data to track price trends.
- **Interactive Dashboard**: Built with Streamlit for exploring market analytics.
- **Investment Opportunity Engine**: Flags undervalued properties based on neighborhood averages.
- **PDF Reports**: Generates market summaries.

## Getting Started

1. Create a virtual environment and install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Initialize database and run the scraper:
   ```bash
   python run_pipeline.py
   ```
3. Run the Streamlit dashboard:
   ```bash
   streamlit run src/dashboard/app.py
   ```
