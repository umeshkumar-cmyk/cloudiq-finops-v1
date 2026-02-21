# Enterprise FinOps Dashboard

**Version:** 1.0.0 | **Built:** February 2026

A professional, modular cloud cost analytics platform built with Python & Streamlit. Provides real-time visibility into cloud spending with anomaly detection, forecasting, and optimization recommendations.

## 🎯 Features

### The 4 Analytics Pillars

| Pillar | Feature | Use Case |
|--------|---------|----------|
| **📈 Descriptive** | Historical analysis, trending, cost breakdown by provider/service/region | Monthly cost reporting, trend analysis |
| **🔍 Diagnostic** | Anomaly detection, cost spike identification, efficiency analysis | Root cause analysis, problem identification |
| **🔮 Predictive** | 12-month cost forecasting using polynomial regression | Budget planning, forecasting |
| **💡 Prescriptive** | Smart optimization recommendations (rightsizing, reserved instances) | Cost optimization roadmap |

### Additional Features

- 🌙 **Dark Mode Charts:** Professional Plotly visualizations optimized for dark theme
- 🔄 **Flexible Connectors:** Pluggable architecture for AWS, Azure, GCP, and SaaS APIs (currently demo mode)
- 📊 **Interactive Dashboard:** Sidebar controls for date ranges, threshold customization
- 📱 **Responsive Design:** Works on desktop, tablet, and mobile devices
- 💾 **CSV-First Approach:** No external database required

---

## 📋 Prerequisites

- **Python:** 3.8+ (3.10+ recommended)
- **OS:** Windows, macOS, Linux
- **Disk Space:** ~500MB for dependencies
- **Internet:** For cloud API connectors (optional, demo data works offline)

---

## 🚀 Quick Start

### 1. Clone or Download Repository
```bash
git clone https://github.com/yourOrg/cloudiq-finops.git
cd cloudiq-finops
```

### 2. Create Virtual Environment
```bash
# On Windows
python -m venv venv
venv\Scripts\activate

# On macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Run Dashboard
```bash
streamlit run app.py
```

Dashboard will open in your browser at `http://localhost:8501`

---

## 📁 Project Structure

```
cloudiq-finops-v1/
├── app.py                          # Main entry point (Streamlit UI)
├── requirements.txt                # Python dependencies
├── .gitignore                      # Git ignore file
│
├── modules/                        # Analytics modules
│   ├── __init__.py                # Package marker
│   ├── data_engine.py             # Data loading & normalization
│   ├── analytics_engine.py        # Anomaly detection, forecasting, recommendations
│   └── visualizer.py              # Plotly chart factory
│
├── data/                          # Data storage
│   └── enterprise_cloud_spend.csv # Sample cloud spending data
│
├── docs/                          # Documentation
│   ├── User_Guide.md              # Non-technical user documentation
│   ├── Architecture.md            # Technical architecture & design
│   └── README.md                  # This file
│
└── config/                        # Configuration (optional, for future use)
    └── secrets.yaml               # Cloud API credentials (git-ignored)
```

---

## 💻 Usage

### For Non-Technical Users (Finance, Management)
1. Open the dashboard
2. Check **📈 Descriptive** tab for monthly cost overview
3. Review **🔍 Diagnostic** tab for anomalies
4. Share **🔮 Predictive** forecast with budget teams
5. Share **💡 Prescriptive** recommendations with engineering

See `docs/User_Guide.md` for detailed instructions.

### For Technical Users (Cloud Engineers, DevOps)
1. Review **🔍 Diagnostic** tab for cost Issues
2. Validate **💡 Prescriptive** recommendations
3. Check **🔗 Connectors** tab for API integration setup
4. Configure cloud API credentials for live data
5. Customize thresholds and models in sidebar

See `docs/Architecture.md` for technical details.

---

## 🔧 Configuration

### Sidebar Settings

**Date Range Filter**
- Filter to specific time period
- Affects all dashboard tabs
- Default: Last 90 days

**Anomaly Detection Threshold**
- Range: 5-50% increase
- Default: 15%
- Lower = more sensitive to spikes

**Forecast Period**
- Range: 3-24 months
- Default: 12 months
- Longer = less accurate but broader view

### Data Configuration

Update `data/enterprise_cloud_spend.csv` with your cloud spending data:

**Required Columns:**
| Column | Type | Example |
|--------|------|---------|
| Date | YYYY-MM-DD | 2026-02-21 |
| Provider | String | AWS, Azure, GCP |
| Service | String | Databricks, Snowflake, Kubernetes |
| Region | String | us-east-1, eastus |
| Amount | Float | 1250.50 |
| Usage_Type | String | on-demand, reserved, spot |
| Efficiency_Score | Float (0-100) | 75 |

---

## 🔌 API Connectors (Future Enhancements)

### Current: Demo Mode
Uses local `enterprise_cloud_spend.csv` for demo/testing

### Planned: Live Integrations

**AWS Cost Explorer**
```python
# Setup:
1. Create IAM user with ce:GetCostAndUsage permission
2. Configure AWS credentials
3. Enable in app.py
```

**Azure Cost Management**
```python
# Setup:
1. Register app in Azure AD
2. Grant "Cost Management Reader" role
3. Configure credentials
```

**GCP BigQuery Billing**
```python
# Setup:
1. Enable BigQuery API
2. Create service account
3. Export billing to BigQuery
```

See `docs/Architecture.md` for implementation examples.

---

## 📊 Dashboard Walkthrough

### 📈 Descriptive Analytics
- **4 KPI Cards:** Total Spend, Avg Monthly, Efficiency, Record Count
- **Cost by Provider:** Pie chart distribution (AWS, Azure, etc.)
- **Cost by Service:** Top services by spend
- **Trending:** Monthly cost trend line
- **Regional Breakdown:** Spend by region
- **Usage Type:** On-demand vs Reserved vs Spot

**Export:** Use Plotly camera icon to save charts as PNG

### 🔍 Diagnostic Analytics
- **Anomaly Detection:** Red flags for cost spikes > threshold
- **Severity Levels:** Critical (>30%), High (>20%), Medium (>threshold)
- **Low Efficiency:** Services with efficiency scores < 50
- **Detailed Table:** Full anomaly details for investigation

**Action:** Investigate critical issues within 24 hours

### 🔮 Predictive Analytics
- **12-Month Forecast:** Historical + projected costs
- **Service Trends:** Individual service trend lines
- **Forecast Accuracy:** Higher for short-term (1-3 months)
- **Metrics:** Current, average forecast, 12-month projection

**Use For:** Budget planning, workload forecasting

### 💡 Prescriptive Analytics
- **Recommendations:** Rightsizing, Reserved Instances, Cleanup
- **Savings Potential:** Estimated monthly/annual savings
- **Priority:** Focus on high-impact items first
- **Detailed Actions:** Specific steps for each recommendation

**Implement:** Start with high-priority, low-risk recommendations

### 🔗 Connectors & Integration
- **Setup Guides:** Step-by-step for each cloud provider
- **Code Examples:** Python implementation samples
- **Connection Status:** Health check for each connector
- **Documentation:** Integration best practices

**For DevOps Team:** Follow setup instructions to enable live data

---

## 🎨 Customization

### Modify Chart Colors

Edit `modules/visualizer.py`:
```python
# Color scheme
PRIMARY_COLOR = "#00D9FF"      # Cyan
SECONDARY_COLOR = "#FF6B6B"    # Red (alerts)
SUCCESS_COLOR = "#51CF66"      # Green
WARNING_COLOR = "#FFD93D"       # Yellow
```

### Adjust Anomaly Algorithm

Edit `modules/analytics_engine.py`:
```python
def detect_anomalies(self, threshold_pct: float = 15.0):
    # Modify baseline calculation or sensitivity
```

### Add New Metrics

Edit `modules/analytics_engine.py`:
```python
def calculate_custom_metric(self):
    # Add your custom metric calculation
    return result
```

---

## 🐛 Troubleshooting

### Issue: "Data file not found"
**Fix:**
1. Ensure `data/enterprise_cloud_spend.csv` exists
2. Verify file path is correct
3. Check file has required columns

### Issue: Charts loading slowly
**Fix:**
1. Reduce date range (sidebar)
2. Filter to specific providers/services
3. Upgrade to larger server instance

### Issue: "No anomalies detected"
**Fix:**
1. Lower anomaly threshold slider
2. Check if data has variability
3. Verify threshold calculation

### Issue: Dashboard won't start
**Fix:**
```bash
# Clear cache
rm -rf .streamlit

# Reinstall dependencies
pip install --upgrade -r requirements.txt

# Run in debug mode
streamlit run app.py --logger.level=debug
```

---

## 📈 Performance Tips

### For Large Datasets (>500K records)
1. Implement data sampling/aggregation
2. Use date range filtering aggressively
3. Consider moving to cloud database
4. Add result caching layer

### For Slow Forecasts
1. Reduce historical data window
2. Lower polynomial degree
3. Use monthly instead of daily data
4. Pre-compute forecasts offline

### For Slow Visualizations
1. Limit data points per chart
2. Enable chart caching
3. Use simpler plot types
4. Aggregate before plotting

---

## 🔐 Security Considerations

### For Production Deployment

1. **Secrets Management**
   - Store API credentials in `.streamlit/secrets.toml` (Streamlit Cloud)
   - Use environment variables for on-premise
   - Never commit credentials to git

2. **Data Privacy**
   - Implement row-level security if sharing across orgs
   - Mask sensitive PII in logs
   - Encrypt data in transit (HTTPS)

3. **Access Control**
   - Use SSO/OAuth if on Streamlit Cloud
   - Implement IP whitelisting for on-premise
   - Audit access logs

4. **.gitignore**
   - Already configured to exclude `config/secrets.yaml`
   - Review `.gitignore` before first commit

---

## 📚 Documentation

- 📘 **User Guide:** `docs/User_Guide.md` (100+ pages for non-technical users)
- 🏗️ **Architecture:** `docs/Architecture.md` (Technical deep-dive)
- 💻 **Code Comments:** Inline docstrings in all modules
- 📊 **Sample Data:** `data/enterprise_cloud_spend.csv` (100+ transactions)

---

## 🛠️ Development

### Adding New Features

1. **New Analytics:** Add method to `AnalyticsEngine` class
2. **New Charts:** Add method to `Visualizer` class
3. **New Data Source:** Extend `DataEngine` class
4. **New Tab:** Add tab logic to `app.py`

### Testing

```bash
# Test data loading
python -c "from modules.data_engine import DataEngine; d = DataEngine(); print(d.load_data())"

# Test analytics
python -c "from modules.analytics_engine import AnalyticsEngine; print('OK')"
```

### Code Style

- Use PEP 8 conventions
- Add docstrings to all functions/classes
- Include type hints where possible
- Add inline comments for complex logic

---

## 📦 Dependencies

| Package | Version | Purpose |
|---------|---------|---------|
| streamlit | 1.28.1+ | Web framework |
| pandas | 2.1.1+ | Data manipulation |
| numpy | 1.24.3+ | Numerical computing |
| plotly | 5.17.0+ | Interactive charts |
| scipy | 1.11.3+ | Statistical functions |

---

## 🚢 Deployment

### Streamlit Cloud
```bash
# Push to GitHub
git push origin main

# Go to https://share.streamlit.io
# Click "New app" → Select repo & main → Deploy
```

### On-Premise (Linux Server)
```bash
# Install Python 3.10+
sudo apt-get install python3.10

# Clone repo
git clone <repo-url>
cd cloudiq-finops-v1

# Setup service
sudo nano /etc/systemd/system/finops.service
# [Service]
# ExecStart=<venv>/bin/streamlit run app.py

# Start service
sudo systemctl start finops
sudo systemctl enable finops
```

### Docker
```dockerfile
FROM python:3.10-slim
WORKDIR /app
COPY . .
RUN pip install -r requirements.txt
EXPOSE 8501
CMD ["streamlit", "run", "app.py"]
```

---

## 🤝 Contributing

1. Fork repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open Pull Request

---

## 📝 License

This project is proprietary and confidential. All rights reserved © 2026 CloudIQ Analytics.

---

## 👥 Support

- 📧 **Email:** finops-team@company.com
- 💬 **Slack:** #finops-dashboard
- 📞 **Phone:** Ext. 1234
- 📚 **Wiki:** confluence.company.com/finops

---

## 🗺️ Roadmap

### v1.1.0 (Q2 2026)
- [ ] Live AWS Cost Explorer integration
- [ ] Live Azure Cost Management integration
- [ ] Custom metric builder
- [ ] Advanced forecasting (ARIMA, Prophet)

### v1.2.0 (Q3 2026)
- [ ] Real-time streaming data
- [ ] SQL query builder
- [ ] Advanced alerting & escalation
- [ ] Team-based dashboards

### v2.0.0 (Q4 2026)
- [ ] Data warehouse integration
- [ ] Enterprise SSO/SAML
- [ ] Advanced ML recommendations
- [ ] Mobile app

---

## 🎓 Credits

**Built by:** CloudIQ Analytics Team  
**Architecture:** Cloud FinOps Best Practices  
**Data:** Sample cloud spending dataset  
**Framework:** Streamlit + Plotly  

---

**Version 1.0.0 | Updated February 21, 2026**
