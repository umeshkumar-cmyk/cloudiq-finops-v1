# Enterprise FinOps Dashboard - User Guide

## Welcome to CloudIQ FinOps

**Version:** 1.0.0 | **Updated:** February 2026

---

## Table of Contents

1. [Getting Started](#getting-started)
2. [Dashboard Overview](#dashboard-overview)
3. [The 4 Analytics Pillars](#the-4-analytics-pillars)
4. [How to Use Each Tab](#how-to-use-each-tab)
5. [Key Metrics Explained](#key-metrics-explained)
6. [Common Questions](#common-questions)
7. [Troubleshooting](#troubleshooting)

---

## Getting Started

### System Requirements
- **Browser:** Chrome, Firefox, Safari, or Edge (any recent version)
- **Internet:** Stable connection recommended
- **Device:** Desktop, Laptop, or Tablet

### Accessing the Dashboard
1. Open your browser
2. Navigate to the dashboard URL provided by your IT team
3. You should see the **Enterprise FinOps Dashboard** homepage
4. No login required (if on internal network)

### First Steps
1. **Check the Sidebar** (left side) for date filters and settings
2. **Review the Overview Tab** to understand your cloud spend
3. **Explore Anomalies** to see if anything unusual is happening
4. **Check Recommendations** for optimization opportunities

---

## Dashboard Overview

### What is FinOps?
FinOps (Financial Operations) is a practice that brings together:
- **Finance Teams** (budgeting & cost control)
- **Engineering Teams** (resource optimization)
- **Operations Teams** (efficiency & monitoring)

### Why This Dashboard?
✅ **See where money is spent** - Cloud cost visibility  
✅ **Find problems early** - Anomaly detection  
✅ **Plan ahead** - Cost forecasting  
✅ **Make smart decisions** - Optimization recommendations  

---

## The 4 Analytics Pillars

The dashboard is built on 4 core analytics concepts:

### 1. **Descriptive** (What happened?)
📈 **Historical analysis** - Reports on past spending patterns
- Total cost, monthly trends, cost by provider/service
- Regional breakdown, usage distribution
- **Goal:** Understand cost structure and trends

### 2. **Diagnostic** (Why did it happen?)
🔍 **Root cause analysis** - Identify problems
- Anomaly detection (cost spikes)
- Low efficiency services
- Cost allocation by dimension
- **Goal:** Find drives of unexpected costs

### 3. **Predictive** (What will happen?)
🔮 **Forecasting** - Project into future
- 12-month cost forecast
- Trend analysis by service
- Seasonal patterns (if data available)
- **Goal:** Budget and plan for next year

### 4. **Prescriptive** (What should we do?)
💡 **Recommendations** - Actionable insights
- Rightsizing opportunities
- Reserved instance recommendations
- Resource cleanup suggestions
- **Goal:** Reduce costs while maintaining performance

---

## How to Use Each Tab

### 📈 Descriptive Analytics Tab
**For:** Understanding overall cloud spending patterns  
**Best For:** Finance managers, monthly reporting

**What You'll See:**
- **Top 4 KPI Cards:** Total Spend, Avg Monthly Spend, Efficiency Score, Total Records
- **Provider Breakdown:** Pie chart showing AWS, Azure, SaaS distribution
- **Service Breakdown:** Which services cost the most (Databricks, Snowflake, etc.)
- **Cost Trend Chart:** Line graph showing costs over time
- **Regional Distribution:** Bar chart of spending by region
- **Usage Type:** How different usage types contribute to costs

**How to Use:**
1. Set date range in sidebar (top left)
2. Read the 4 KPI cards for quick overview
3. Scan pie charts to see distribution
4. Review trend chart for seasonal patterns
5. Share with finance team for monthly reviews

**Example Insights:**
- "AWS represents 60% of cloud costs"
- "Costs increased 15% month-over-month"
- "Kubernetes is our biggest expense by service"

---

### 🔍 Diagnostic Analytics Tab
**For:** Finding cost problems and inefficiencies  
**Best For:** Cloud engineers, ops managers

**What You'll See:**
- **Anomaly Detection:** Red flags for unusual cost spikes
- **Severity Indicators:** Critical (>30%), High (>20%), Medium (>threshold)
- **Anomaly Breakdown:** Table showing affected services/regions
- **Low Efficiency Services:** Scatter plot showing waste potential
- **Cost at Risk:** Summary of underperforming resources

**How to Use:**
1. **Start with anomaly count** - How many issues detected?
2. **Review critical items first** - These need immediate attention
3. **Click each anomaly** for details: which service, region, how much change
4. **Examine low-efficiency services** - Resources not being used effectively
5. **Prioritize action items** - Focus on highest impact issues

**Example Insights:**
- "Snowflake costs jumped 45% this week (CRITICAL)"
- "Kubernetes in us-east-1 showing low efficiency (38/100)"
- "Azure VM costs increased 28% (HIGH)"

**What to Do:**
- 🟥 **Critical:** Investigate immediately, may have misconfiguration
- 🟠 **High:** Schedule investigation within 48 hours
- 🟡 **Medium:** Monitor, may be temporary spike

---

### 🔮 Predictive Analytics Tab
**For:** Budget planning and forecasting  
**Best For:** CFO, finance planners, budget owners

**What You'll See:**
- **Forecast Chart:** Blue line (historical) + Yellow dashed (forecast)
- **Current Month Spend:** Actual spend this month
- **Avg Forecasted Spend:** Average monthly from now to 12 months out
- **12-Month Projection:** Final month forecast value
- **Service Trends:** How individual services are expected to grow

**How to Use:**
1. **Check the main forecast chart** - Does trend look reasonable?
2. **Compare current vs projected** - Will costs increase or decrease?
3. **Adjust forecast periods** slider for different horizons (3-24 months)
4. **Select specific services** to drill into details
5. **Use for budget planning** - Share 12-month projection with finance

**Example Insights:**
- "Costs will grow ~12% over next 12 months"
- "Databricks showing steeper growth (20% annually)"
- "Snowflake costs stabilizing (flat forecast)"

**What It Means:**
- 📈 **Upward trend:** Demand increasing, costs rising
- 📊 **Flat trend:** Steady state, stable budget
- 📉 **Downward trend:** Optimization working, costs falling

---

### 💡 Prescriptive Analytics Tab
**For:** Finding cost savings opportunities  
**Best For:** Cloud architects, cost optimization team

**What You'll See:**
- **Recommendation Count:** How many optimization opportunities
- **High Priority Items:** Most impactful actions
- **Total Savings Potential:** How much money can be saved
- **Recommendation Types:**
  - 🔧 **Rightsizing:** Resources bigger than needed
  - 💾 **Reserved Instances:** Buying commitments for discounts
  - 🗑️ **Resource Cleanup:** Terminating unused services

**How to Use:**
1. **Start with totals** - Total savings potential tells story
2. **Filter by recommendation type** dropdown
3. **Click expanders** to see detailed actions
4. **Review priority** - Focus on "High" first
5. **Write down actions** and assign to teams

**Recommendation Details Include:**
- Current spend (how much spending now)
- Potential savings (estimate of savings possible)
- Priority (High/Medium impact)
- Efficiency score (0-100, lower = bigger issue)
- Specific action to take

**Example Insights:**
- "Rightsize Databricks: Save $15K/month by using smaller instance type"
- "Buy Azure Reserved: Save $8K/month with 1-year commitment"
- "Clean up unused VMs: Save $2K/month immediate"

**Next Steps:**
1. ✅ Evaluate savings claim with your team
2. 🧪 Test in non-prod if possible
3. 📋 Add to optimization roadmap
4. 📊 Track actual savings after implementation

---

### 🔗 Connectors & Integration Tab
**For:** Connecting to cloud provider APIs  
**Best For:** DevOps, cloud admins, IT infrastructure

**What You'll See:**
- **Integration Methods:** AWS, Azure, GCP, SaaS connectors
- **Setup Instructions:** Step-by-step to connect APIs
- **Code Examples:** For developers implementing connections
- **Connection Status:** Success/failure indicators
- **Supported Services:** Which platforms currently integrated

**How to Use (Technical Users):**
1. **Select your cloud provider** (AWS, Azure, etc.)
2. **Follow setup instructions** (create credentials, assign permissions)
3. **Configure credentials** in secrets file
4. **Test connection** - dashboard should show "connected"
5. **Verify data sync** - check that new data appears in 1-2 hours

**How to Use (Non-Technical Users):**
1. Show this tab to your IT team
2. Ask them to "Set up live cloud integration"
3. Once connected, dashboard auto-updates with real costs
4. You don't need to upload CSV files anymore

**Future Feature Note:**
Currently showing **demo/sample data**. Live integration coming in v1.1.

---

## Key Metrics Explained

### Total Cloud Spend
**Definition:** Sum of all cloud costs in selected period  
**Example:** $450,000 for the month  
**Why It Matters:** Total budget commitment, baseline for tracking

### Month-over-Month (MoM) Change
**Definition:** Percentage increase/decrease vs previous month  
**Example:** +15% MoM  
**Why It Matters:** Trend indicator - are costs growing or shrinking?  
**Green is good:** Negative % = declining costs  
**Red is bad:** High positive % = rapid cost growth

### Efficiency Score
**Definition:** 0-100 scale indicating resource utilization  
**0-30:** Severe waste (immediate action)  
**31-50:** Inefficient (optimization needed)  
**51-75:** Good (maintain current usage)  
**76-100:** Excellent (highly optimized)

### Unit Economics
**Definition:** Cost per unit of work  
**Example:** $100 per million API calls  
**Why It Matters:** Compare efficiency across services  
**Use For:** Identifying which services give best value

### Potential Savings
**Definition:** Estimated money that could be saved if recommendation implemented  
**Example:** $15,000/month  
**Important:** These are estimates - confirm with teams before commitment

---

## Common Questions

### Q: How often is data updated?
**A:** 
- **CSV Upload:** Manual refresh (click button in sidebar)
- **Live API:** Typically 2-4 hours behind actual (cloud provider delay)
- **Forecast:** Re-calculates when data refreshed

### Q: What if I see an anomaly that looks normal?
**A:** Anomalies are statistical alerts, not always problems
- **Legitimate reasons:** Increase in actual usage, planned capacity increase
- **Action:** Investigate the root cause, confirm with team
- **Adjust:** If recurring, we can adjust sensitivity slider

### Q: How accurate are forecasts?
**A:** 
- **Short term (1-3 months):** Usually 85-90% accurate
- **Medium term (3-6 months):** Around 75-85% accurate
- **Long term (6-12+ months):** 60-75% accurate
- **Affects:** Seasonal variations, new projects, growth/shrinkage

**Better predictions when:**
- ✅ Consistent historical pattern
- ✅ No major changes planned
- ✅ At least 6-12 months of data

### Q: How are recommendations prioritized?
**A:** By total potential savings impact
- Highest savings = show first
- High priority = $10K+ monthly potential
- Medium priority = $1K-10K monthly potential

### Q: Can I share this dashboard?
**A:** Yes!
- **Screenshot metrics** for slide decks
- **Record screen** for presentations
- **Export data** (download buttons on some charts)
- **Share link** with other team members (if dashboard is shared)

### Q: What if data looks wrong?
**A:** Check these first:
1. **Date range** - Did you filter correctly?
2. **Last data refresh** - Is data current?
3. **Provider selection** - Did you select all providers?
4. **File contents** - Check data/enterprise_cloud_spend.csv

---

## Troubleshooting

### Issue: "Data file not found"
**Cause:** CSV file missing or in wrong location  
**Fix:** 
1. Check file exists: `data/enterprise_cloud_spend.csv`
2. Verify columns: Date, Provider, Service, Region, Amount, Usage_Type, Efficiency_Score
3. Click "Refresh Data" button

### Issue: Charts are loading slowly
**Cause:** Large dataset or network latency  
**Fix:**
1. Reduce date range (sidebar)
2. Refresh browser
3. Use simpler charts (bars vs scatter)

### Issue: "No anomalies detected" (but I expect some)
**Cause:** Threshold too high or data too consistent  
**Fix:**
1. Adjust anomaly threshold down (sidebar slider)
2. Check if baseline calculation correct
3. Verify data has variability

### Issue: Forecast looks wrong
**Cause:** Limited data or extreme outliers  
**Fix:**
1. Ensure at least 6 months historical data
2. Check for data errors (check Descriptive tab)
3. Review for one-time events (migrations, etc.)

### Issue: Recommendations don't make sense
**Cause:** Business context not captured in algorithm  
**Fix:**
1. Review the efficiency score calculation
2. Consider planned architecture changes
3. Validate with cloud architect

### Issue: Dashboard won't load
**Cause:** Browser cache, Python error, or network  
**Fix:**
1. Hard refresh (Ctrl+Shift+R or Cmd+Shift+R)
2. Clear browser cache
3. Try different browser
4. Check internet connection
5. Contact IT support with error message

---

## Tips & Best Practices

### 📊 Dashboard Best Practices
1. **Review weekly** - Stay aware of cost trends
2. **Share monthly** - Present to finance & tech teams
3. **Act on anomalies** - Don't ignore red alerts
4. **Validate recommendations** - Test before implementing
5. **Track savings** - Document actual impact of changes

### 💰 Cost Optimization Tips
1. **Rightsize first** - Quick wins, low risk
2. **Use Reserved Instances** - Stable workloads
3. **Auto-scale** - Pay only for what you use
4. **Spot instances** - Batch jobs, non-critical work
5. **Clean up regularly** - Delete unused resources

### 📈 Forecasting Tips
1. **Plan quarterly** - Review Q1, Q2, Q3, Q4 separately
2. **Add buffer** - Budget 10-15% above forecast
3. **Review assumptions** - Will headcount change?
4. **Track vs actual** - Compare forecast to reality
5. **Adjust model** - Update forecast with learnings

---

## Getting Help

### For Dashboard Questions
📧 **Email:** finops-team@company.com  
📞 **Slack:** #finops-dashboard  
📚 **Wiki:** confluence.company.com/finops

### For Cost Optimization Help
👥 **Meet the FinOps Team:** Schedule time with cloud architects  
📋 **Request Engagement:** Submit optimization request form  
🚀 **Training:** Join monthly "Cost Optimization 101" webinar

---

## Appendix: Quick Reference

### Key Shortcuts
- **Sidebar visible?** Click > icon if hidden
- **Want to zoom chart?** Click and drag on chart area
- **Download chart?** Hover top-right of chart, click camera icon
- **Date range reset?** Click ↻ icon in date picker

### Column Definitions
| Column | Definition | Example |
|--------|-----------|---------|
| **Date** | Transaction date | 2026-02-15 |
| **Provider** | Cloud vendor | AWS, Azure, GCP |
| **Service** | Service name | Databricks, Snowflake |
| **Region** | Geographic region | us-east-1, europe-west-1 |
| **Amount** | Daily cost in $USD | 1,250.50 |
| **Usage_Type** | How used | on-demand, reserved, spot |
| **Efficiency_Score** | 0-100 utilization score | 85 |

### Useful Formulas
- **MoM Change % = ((Current - Previous) / Previous) × 100**
- **Savings Potential = Current Spend × Savings Rate**
- **Cost per Unit = Total Spend / Volume Metric**

---

**Last Updated:** February 21, 2026  
**Created By:** CloudIQ Analytics Team  
**Version:** 1.0.0
