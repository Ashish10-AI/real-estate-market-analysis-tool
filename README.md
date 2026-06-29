# Real Estate Market Analyzer 🏠

**Analyze property trends, identify best-value neighborhoods, and make data-driven real estate investment decisions.**

![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-Cloud-red.svg)
![Status](https://img.shields.io/badge/Status-Active-success.svg)

---

## 🔴 LIVE DASHBOARD

### **[👉 CLICK HERE TO OPEN INTERACTIVE DASHBOARD 👈](https://ashish10-ai-real-estate-market-analysis-tool-hhhkeacre7bbchrnq.streamlit.app/)**

*Explore 5,000+ property listings, market trends, and investment opportunities in real-time*

---

## ✨ Features at a Glance

✅ **Automated Web Scraper** - Collects 5,000+ property listings daily from MagicBricks  
✅ **SQLite Database** - Persistent storage with historical price tracking  
✅ **Interactive Dashboard** - 5-tab Streamlit interface with real-time analytics  
✅ **Market Intelligence** - Locality analysis, price trends, best-value finder  
✅ **Investment Insights** - Identifies undervalued neighborhoods with high demand  
✅ **Amenities Analysis** - Discover which amenities drive property values  
✅ **Price Trends** - Track market movements over time  
✅ **Daily Updates** - Automated scraping via GitHub Actions (no manual work)  

---

## 📊 Dashboard Overview

The dashboard has 5 interactive tabs:

**1. 📊 City Overview**
- Total properties, average prices, market metrics
- Price distribution histogram
- Key market statistics at a glance

**2. 📍 Locality Analysis**
- Neighborhood-by-neighborhood breakdown
- Min/max/average prices per locality
- Property counts and amenities
- Sortable, searchable data

**3. 💎 Best Value Finder**
- Identifies high-demand + low-price neighborhoods
- Investment opportunity scoring
- Shows which areas are trending up
- Value score for each locality

**4. 📈 Price Trends**
- Historical price movements over 30+ days
- Filter by city or specific neighborhood
- Visualize market appreciation/depreciation
- Identify patterns and opportunities

**5. 🏘️ Detailed Insights**
- Bedroom-wise price analysis (1BHK, 2BHK, etc.)
- Most popular amenities
- Property type distribution
- Market segmentation breakdown

---

## 🛠️ Technology Stack

| Layer | Technology | What it does |
|-------|-----------|-------------|
| **Backend** | Python 3.9+ | Core development language |
| **Data Collection** | BeautifulSoup4, Requests | Scrapes MagicBricks listings |
| **Data Processing** | Pandas, NumPy | Cleans and transforms data |
| **Storage** | SQLite3 | Stores 5K+ properties & trends |
| **Frontend** | Streamlit | Interactive web dashboard |
| **Visualization** | Plotly | Interactive charts & graphs |
| **Deployment** | Streamlit Cloud | Free live hosting |
| **Automation** | GitHub Actions | Runs scraper daily automatically |
| **Version Control** | Git/GitHub | Code management |

---

## 📁 Project Structure

```
real-estate-market-analysis-tool/
│
├── app.py                         # Main Streamlit dashboard
├── scraper.py                     # Web scraper for MagicBricks
├── database.py                    # SQLite database setup
├── analysis.py                    # Data analysis functions
│
├── requirements.txt               # Python dependencies
├── .gitignore                     # Git ignore rules
├── README.md                      # This file
├── LICENSE                        # MIT License
│
├── data/
│   └── properties.db             # SQLite database (auto-created)
│
└── .github/
    └── workflows/
        └── scrape-daily.yml      # GitHub Actions automation
```

---

## 🚀 Quick Start

### Run Locally

**1. Clone the repository**
```bash
git clone https://github.com/Ashish10-AI/real-estate-market-analysis-tool.git
cd real-estate-market-analysis-tool
```

**2. Create virtual environment**
```bash
# Mac/Linux
python3 -m venv venv
source venv/bin/activate

# Windows
python -m venv venv
venv\Scripts\activate
```

**3. Install dependencies**
```bash
pip install -r requirements.txt
```

**4. Scrape data**
```bash
python scraper.py
```
*(First run: 2-3 minutes. Gets 5,000+ properties)*

**5. Run dashboard**
```bash
streamlit run app.py
```

Dashboard opens at: **http://localhost:8501**

---

## 📊 How It Works

### Data Flow

```
MagicBricks Website
        ↓
Web Scraper (BeautifulSoup)
Extract: price, area, location, amenities
        ↓
Data Processing (Pandas)
Parse prices, calculate price/sqft
        ↓
SQLite Database
Store properties & daily snapshots
        ↓
Analysis Engine
Calculate trends, find best-value areas
        ↓
Streamlit Dashboard
Interactive visualizations with Plotly
```

### Key Components

**Scraper (scraper.py)**
- Extracts property listings from MagicBricks
- Handles multiple cities (Dehradun, Bangalore, Delhi)
- Parses: price, area, location, amenities, bedrooms
- Error handling and retry logic
- Rate limiting to avoid blocking

**Database (database.py)**
- SQLite3 schema with 3 normalized tables
- properties: Individual listings
- price_history: Daily price snapshots
- locality_stats: Aggregated statistics
- Optimized queries for fast analytics

**Analysis (analysis.py)**
- 10+ data analysis functions
- Locality statistics & comparisons
- Price trend calculations
- Best-value neighborhood identification
- Amenities analysis

**Dashboard (app.py)**
- Streamlit web application
- 5 interactive tabs
- Plotly visualizations
- Real-time filtering
- Mobile responsive

---

## 📈 Key Metrics

| Metric | Value |
|--------|-------|
| **Properties Scraped** | 5,000+ |
| **Cities Covered** | 3 (Dehradun, Bangalore, Delhi) |
| **Data Points per Property** | 13 |
| **Analysis Functions** | 10+ |
| **Dashboard Tabs** | 5 |
| **Update Frequency** | Daily (Automated) |
| **Database Size** | ~15 MB |
| **Dashboard Load Time** | <2 seconds |

---

## 🔍 Use Cases

**Real Estate Investors**
- Find undervalued neighborhoods
- Track market appreciation
- Identify investment opportunities

**Property Buyers**
- Compare prices across locations
- Research neighborhoods
- Track market trends

**Market Researchers**
- Analyze real estate trends
- Understand price drivers
- Study amenity value

**Data Enthusiasts**
- Learn web scraping
- Practice SQL queries
- Explore data visualization
- Build portfolio projects

---

## 🐛 Troubleshooting

### "ModuleNotFoundError: No module named 'streamlit'"
```bash
pip install -r requirements.txt
```

### "Database is locked"
```bash
rm data/properties.db
python scraper.py  # Recreate database
```

### Scraper not fetching data
- Check internet connection
- MagicBricks may have changed HTML structure
- Check console for specific errors

### Dashboard very slow
- Clear browser cache
- Restart Streamlit: Ctrl+C, then run again
- Try refreshing the page

---

## 🔄 Automated Updates

This project uses **GitHub Actions** to run the scraper automatically every day.

**View automation status:**
1. Go to GitHub repo → "Actions" tab
2. See "Daily Real Estate Scrape" workflow
3. Check latest run status

**How it works:**
- Runs at 00:00 UTC every day
- Scrapes latest property listings
- Updates SQLite database
- No manual intervention needed

---

## 📝 License

This project is licensed under the **MIT License**.

This means:
- ✅ You can use it freely
- ✅ You can modify it
- ✅ You can distribute it
- ✅ Just give credit to the original author

See [LICENSE](LICENSE) file for full details.

---

## 👤 Author

**Ashish Yadav**

- 🎓 **B.Tech Information Technology** - College of Engineering Roorkee (COER), Dehradun
- 📅 **Graduating:** June 2026
- 💼 **Role:** Data Analyst | Python Developer | Creative Technologist

### Connect with me:

- 🔗 **GitHub:** [github.com/Ashish10-AI](https://github.com/Ashish10-AI)
- 🌐 **Portfolio:** [ashishyadav-portfolio.netlify.app](https://ashishyadav-portfolio.netlify.app)
- 💼 **LinkedIn:** [linkedin.com/in/ashish-yadav](https://linkedin.com/in/ashish-yadav)
- 📧 **Email:** ashishff2005@gmail.com

---

## ⭐ Support This Project

If you found this helpful:
- ⭐ Star the repository
- 🍴 Fork and contribute
- 💬 Share feedback
- 📢 Mention it in your projects

---

## 🤝 Contributing

Want to improve this project? We welcome contributions!

1. **Fork the repository**
2. **Create feature branch:** `git checkout -b feature/amazing-feature`
3. **Make your changes**
4. **Commit:** `git commit -m 'Add amazing feature'`
5. **Push:** `git push origin feature/amazing-feature`
6. **Open Pull Request**

### Areas to contribute:
- Bug fixes and optimizations
- New analysis functions
- Additional data sources
- Documentation improvements
- Dashboard UI enhancements
- Performance optimization

---

## 🔮 Future Enhancements

- [ ] Rent yield analysis (rental income vs property price)
- [ ] Price prediction using machine learning
- [ ] Investment ROI calculator
- [ ] SMS/Email alerts for price drops
- [ ] Multi-city comparison tools
- [ ] PostgreSQL backend for scalability
- [ ] Advanced filtering (by amenities, age, etc.)
- [ ] RESTful API endpoints
- [ ] Mobile app version
- [ ] Real-time notifications

---

## 📊 Project Statistics

- **Total Properties Analyzed:** 5,000+
- **Cities Covered:** 3
- **Analysis Functions:** 10+
- **Dashboard Tabs:** 5
- **Data Points per Property:** 13
- **Update Frequency:** Daily
- **Python Lines of Code:** 1,200+
- **Development Time:** 20 hours

---

## 📚 Technologies & Skills Demonstrated

This project showcases:
- ✅ Web scraping (BeautifulSoup4)
- ✅ Data processing (Pandas, NumPy)
- ✅ Database design (SQLite)
- ✅ Data visualization (Streamlit, Plotly)
- ✅ Automation (GitHub Actions)
- ✅ Version control (Git/GitHub)
- ✅ Deployment (Streamlit Cloud)
- ✅ SQL queries
- ✅ Python best practices
- ✅ Error handling & logging

---

## 📞 Support & Feedback

- **Found a bug?** [Open an Issue](https://github.com/Ashish10-AI/real-estate-market-analysis-tool/issues)
- **Have suggestions?** [Start a Discussion](https://github.com/Ashish10-AI/real-estate-market-analysis-tool/discussions)
- **Questions?** Email: ashishff2005@gmail.com

---

## ⚖️ Disclaimer

This project is for **educational and informational purposes**. Real estate investment decisions should be made after thorough research and consultation with financial advisors. The author is not responsible for investment decisions based on this data.

---

## 🙏 Acknowledgments

- **MagicBricks** - For providing property listing data
- **Streamlit** - For the easy-to-use data app framework
- **Plotly** - For interactive visualization library
- **Open Source Community** - For tools and inspiration

---

**Last Updated:** June 2024  
**Status:** ✅ Active Development  
**Version:** 1.0.0  

---

## 🚀 Quick Links

- **[Live Dashboard](https://ashish10-ai-real-estate-market-analysis-tool-hhhkeacre7bbchrnq.streamlit.app/)**
- **[GitHub Repository](https://github.com/Ashish10-AI/real-estate-market-analysis-tool)**
- **[Portfolio Website](https://ashishyadav-portfolio.netlify.app)**
- **[LinkedIn Profile](https://linkedin.com/in/ashish-yadav)**

---

**Made with ❤️ by Ashish Yadav**

**Happy analyzing! 🏠📊**
