# Enterprise FinOps Dashboard - Architecture Guide

## System Architecture Overview

The Enterprise FinOps Dashboard follows a modular, layered architecture designed for scalability, maintainability, and extensibility.

```
┌─────────────────────────────────────────────────────────────────┐
│                        User Interface (UI)                       │
│              Streamlit Web Application (app.py)                  │
│  ┌─────────┬──────────┬──────────┬──────────┬───────────────┐  │
│  │Descript.│Diagnost. │Predictv.│Prescript.│ Connectors    │  │
│  │Analytics│Analytics │Analytics│Analytics │ & Integration │  │
│  └─────────┴──────────┴──────────┴──────────┴───────────────┘  │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│                    Analytics Layer (Modules)                     │
│  ┌──────────────────┐ ┌──────────────┐ ┌──────────────────┐    │
│  │ Data Engine      │ │ Analytics    │ │  Visualizer      │    │
│  │ - Load CSV       │ │ - Anomalies  │ │ - Charts (Dark)  │    │
│  │ - Normalize      │ │ - Forecasts  │ │ - KPI Cards      │    │
│  │ - Filter         │ │ - Optimize   │ │ - Heatmaps       │    │
│  │ - Aggregate      │ │ - Diagnostics│ │ - Trends         │    │
│  └──────────────────┘ └──────────────┘ └──────────────────┘    │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│                        Data Layer                                │
│  ┌──────────────┐  ┌──────────────┐  ┌─────────────────┐       │
│  │   CSV File   │  │  In-Memory   │  │ Future: Cloud   │       │
│  │ (Primary)    │  │  DataFrames  │  │ APIs (AWS/Azure)│       │
│  └──────────────┘  └──────────────┘  └─────────────────┘       │
└─────────────────────────────────────────────────────────────────┘
```

## Data Flow Pipeline

### 1. **Ingestion Stage**
- **Source:** CSV file (`data/enterprise_cloud_spend.csv`)
- **Format:** Comma-separated values with headers
- **Required Columns:** Date, Provider, Service, Region, Amount, Usage_Type, Efficiency_Score
- **Processing:** Pandas `read_csv()` with error handling

### 2. **Normalization Stage**
- **Date Conversion:** Parse Date to datetime64
- **Amount Validation:** Ensure numeric type, handle missing values
- **Efficiency Scoring:** Validate range (0-100)
- **Deduplication:** Remove null critical values
- **Sorting:** Order by date for time-series consistency

### 3. **Analysis Stage**

#### Descriptive Analytics
```python
DataEngine.get_summary_statistics()  # Overall KPIs
DataEngine.get_monthly_spend()       # Time-series aggregation
DataEngine.get_spend_by_provider()   # Provider breakdown
DataEngine.get_spend_by_service()    # Service breakdown
```

#### Diagnostic Analytics
```python
AnalyticsEngine.detect_anomalies()              # Spike detection
AnalyticsEngine.get_efficiency_low_services()  # Low performers
AnalyticsEngine.calculate_mom_change()          # Month-over-month
```

#### Predictive Analytics
```python
AnalyticsEngine.forecast_spend()    # 12-month polynomial regression
AnalyticsEngine.get_cost_trend()    # Trend analysis by dimension
```

#### Prescriptive Analytics
```python
AnalyticsEngine.generate_optimization_recommendations()  # Actions
```

### 4. **Visualization Stage**
- **Framework:** Plotly (interactive, dark-mode optimized)
- **Charts:** Line, Bar, Pie, Scatter, Heatmap, Anomaly Highlight
- **Theme:** Dark background (#0f1419), Cyan highlights (#00D9FF)

### 5. **Presentation Stage**
- **Framework:** Streamlit
- **Layout:** Wide-mode with sidebar navigation
- **Interaction:** Date filters, threshold sliders, multi-select dropdowns
- **Performance:** Session state caching for data loading

---

## Module Reference

### `data_engine.py` - DataEngine Class
**Responsibility:** Data ingestion, cleaning, and aggregation

**Key Methods:**
| Method | Purpose |
|--------|---------|
| `load_data()` | Load and validate CSV |
| `_normalize_data()` | Clean and standardize data |
| `filter_by_date_range()` | Temporal filtering |
| `get_monthly_spend()` | Monthly aggregation |
| `get_spend_by_provider()` | Provider breakdown |
| `get_spend_by_service()` | Service breakdown |
| `get_efficiency_low_services()` | Filter underperformers |
| `get_summary_statistics()` | Overall KPIs |

---

### `analytics_engine.py` - AnalyticsEngine Class
**Responsibility:** Statistical analysis, ML models, and recommendations

**Key Methods:**
| Method | Purpose | Algorithm |
|--------|---------|-----------|
| `detect_anomalies()` | Cost spike detection | Statistical deviation + threshold |
| `forecast_spend()` | 12-month projection | Polynomial Regression (numpy.polyfit) |
| `get_cost_trend()` | Dimensional trend analysis | Time-series aggregation |
| `generate_optimization_recommendations()` | Action items | Rule-based heuristics |
| `calculate_mom_change()` | Month-over-month delta | Percentage change |

**Anomaly Detection Logic:**
```
1. Group data by Service + Date
2. Calculate baseline (mean of historical)
3. Compare current vs baseline
4. Flag if change > threshold_pct
5. Classify severity (Critical > 30%, High > 20%, Medium > threshold)
```

**Forecasting Logic:**
```
1. Aggregate to monthly level
2. Fit polynomial (degree 2 default)
3. Project X months into future
4. Return historical + forecast combined
```

**Optimization Rules:**
```
- Low Efficiency (< 50)  → Rightsizing
- High Usage + High Eff  → Reserved Instances
- Low Usage + High Cost  → Resource Cleanup
```

---

### `visualizer.py` - Visualizer Class
**Responsibility:** Professional Plotly chart generation

**Chart Types:**
| Chart | Use Case |
|-------|----------|
| `create_kpi_card()` | Metric display with delta |
| `create_time_series()` | Trend visualization |
| `create_bar_chart()` | Categorical comparison |
| `create_pie_chart()` | Composition analysis |
| `create_scatter_plot()` | Correlation analysis |
| `create_forecast_chart()` | Historical + projection |
| `create_anomaly_highlight()` | Spike visualization |
| `create_heatmap()` | 2D dimensional analysis |

**Dark Mode Configuration:**
- Template: `plotly_dark`
- Paper Background: `rgba(20, 33, 61, 0.8)`
- Plot Background: `rgba(20, 33, 61, 0.8)`
- Primary Color: `#00D9FF` (Cyan)
- Alert Color: `#FF6B6B` (Red)
- Success Color: `#51CF66` (Green)

---

## Configuration & Customization

### Sidebar Controls
```python
start_date               # Date range start
end_date                # Date range end
anomaly_threshold       # Anomaly detection sensitivity (5-50%)
forecast_periods        # Forecast horizon (3-24 months)
```

### Tuning Parameters
- **Efficiency Threshold:** 50 (default for low-efficiency flag)
- **Anomaly Sensitivity:** 15% (default)
- **Forecast Polynomial Degree:** 2 (quadratic)
- **Savings Assumption:** 20-25% (varies by recommendation type)

---

## Integration Points (Future)

### Cloud API Adapters
Currently using mock/sample data. To enable live integrations:

**AWS Cost Explorer:**
```python
class AWSConnector:
    def fetch_costs(self):
        # API call to get_cost_and_usage
        # Map to schema: Date, Provider, Service, Region, Amount, ...
```

**Azure Cost Management:**
```python
class AzureConnector:
    def fetch_costs(self):
        # API call to Cost Management Query
        # Map to schema
```

**GCP BigQuery Billing:**
```python
class GCPConnector:
    def fetch_costs(self):
        # Query BigQuery billing export
        # Map to schema
```

### Adapter Pattern
All connectors should implement:
```python
class BaseConnector:
    def authenticate(self): pass
    def fetch_costs(self, start_date, end_date) -> pd.DataFrame: pass
    def normalize_schema(self) -> pd.DataFrame: pass
```

---

## Performance Considerations

### Caching Strategy
- DataEngine loading cached with `@st.cache_resource`
- Prevents re-reading CSV on every interaction
- Clear cache on manual refresh

### Data Limits
- Recommended: < 500K records
- Current dashboard: ~5K sample records
- Scaling: Implement chunking for > 1M records

### Optimization Tips
- Filter by date range early (sidebar)
- Aggregate to monthly for trend analysis
- Use vectorized pandas operations
- Cache forecast results

---

## Error Handling

### Data Validation
- ✅ FileNotFoundError → User-friendly message
- ✅ Missing columns → Schema validation error
- ✅ Type mismatches → Auto-conversion with fallback
- ✅ Null values → Row removal or default treatment

### User Feedback
- 🎯 Info boxes: Configuration guidance
- ⚠️ Warning boxes: Data quality issues
- ❌ Error boxes: Fatal errors with recovery steps
- ✅ Success messages: Anomaly-free periods

---

## Deployment Checklist

- [ ] Install dependencies: `pip install -r requirements.txt`
- [ ] Prepare CSV file: `data/enterprise_cloud_spend.csv`
- [ ] Verify column names match schema
- [ ] Test locally: `streamlit run app.py`
- [ ] Configure API credentials (if using live connectors)
- [ ] Deploy to Streamlit Cloud or on-premise
- [ ] Set environment variables for production

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2026-02-21 | Initial release with 4 analytics pillars |
| 1.1.0 | TBD | Live AWS/Azure integration |
| 1.2.0 | TBD | Advanced ML forecasting (ARIMA, Prophet) |
| 2.0.0 | TBD | Real-time streaming & data warehouse integration |

---

## Support & Documentation

- 📘 **User Guide:** `/docs/User_Guide.md`
- 🏗️ **Architecture:** This file
- 💻 **Code Comments:** Inline docstrings in each module
- 📊 **Examples:** Sample data in `data/enterprise_cloud_spend.csv`
