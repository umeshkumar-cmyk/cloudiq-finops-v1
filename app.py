"""
Enterprise FinOps Dashboard - Main Application
Professional cloud cost analytics and optimization platform
"""

import streamlit as st
import pandas as pd
import numpy as np
import io
from datetime import datetime, timedelta
from modules.data_engine import DataEngine
from modules.analytics_engine import AnalyticsEngine
from modules.visualizer import Visualizer


# ============================================================================
# PAGE CONFIGURATION
# ============================================================================

st.set_page_config(
    page_title="Enterprise FinOps Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================================
# CUSTOM STYLING
# ============================================================================

st.markdown("""
<style>
    /* Dark theme customization */
    .main {
        background-color: #0f1419;
    }
    
    .sidebar .sidebar-content {
        background-color: #101820;
    }
    
    /* Custom card styling */
    .metric-card {
        background: linear-gradient(135deg, #1a2940 0%, #0f1e3f 100%);
        padding: 20px;
        border-radius: 10px;
        border-left: 4px solid #00D9FF;
        margin-bottom: 10px;
    }
    
    /* Alert styling */
    .alert-critical {
        background-color: rgba(255, 107, 107, 0.2);
        border-left: 4px solid #FF6B6B;
        padding: 10px;
        border-radius: 5px;
    }
    
    .alert-warning {
        background-color: rgba(255, 217, 61, 0.2);
        border-left: 4px solid #FFD93D;
        padding: 10px;
        border-radius: 5px;
    }
</style>
""", unsafe_allow_html=True)

# ============================================================================
# SESSION STATE INITIALIZATION
# ============================================================================

if 'data_engine' not in st.session_state:
    st.session_state.data_engine = None
if 'analytics_engine' not in st.session_state:
    st.session_state.analytics_engine = None
if 'data_loaded' not in st.session_state:
    st.session_state.data_loaded = False


# ============================================================================
# SIDEBAR CONFIGURATION
# ============================================================================

with st.sidebar:
    st.image("https://via.placeholder.com/200x60?text=CloudIQ+FinOps", width=300)
    st.markdown("---")
    
    st.subheader("� Data Upload")
    
    # File uploader
    uploaded_file = st.file_uploader(
        "Upload Cloud Spend CSV",
        type="csv",
        help="Upload your enterprise_cloud_spend.csv file"
    )
    
    st.markdown("---")
    
    st.subheader("�🔧 Configuration")
    
    # Date range selector
    col1, col2 = st.columns(2)
    with col1:
        start_date = st.date_input("Start Date", datetime.now() - timedelta(days=90))
    with col2:
        end_date = st.date_input("End Date", datetime.now())
    
    st.markdown("---")
    
    # Anomaly detection threshold
    anomaly_threshold = st.slider(
        "Anomaly Detection Threshold (%)",
        min_value=5,
        max_value=50,
        value=15,
        step=5,
        help="Flag cost increases above this percentage"
    )
    
    # Forecast periods
    forecast_periods = st.slider(
        "Forecast Period (Months)",
        min_value=3,
        max_value=24,
        value=12,
        step=1
    )
    
    st.markdown("---")
    
    # Data refresh
    if st.button("🔄 Refresh Data", key="refresh_btn", use_container_width=True):
        st.session_state.data_loaded = False
        st.rerun()
    
    st.markdown("---")
    st.markdown("**Dashboard Version:** 1.0.0  \n**Last Updated:** 2026-02-21")


# ============================================================================
# MAIN CONTENT AREA
# ============================================================================

st.title("📊 Enterprise FinOps Dashboard")
st.markdown("*Real-time cloud cost analytics, anomaly detection & optimization insights*")

# ============================================================================
# DATA LOADING
# ============================================================================

@st.cache_resource
def load_data(file_path=None):
    """Load data using DataEngine with caching."""
    try:
        engine = DataEngine(file_path)
        df = engine.load_data()
        return engine, df
    except FileNotFoundError as e:
        st.error(f"❌ Error: {str(e)}")
        st.info("📝 Please ensure CSV file exists with columns: Date, Provider, Service, Region, Amount, Usage_Type, Efficiency_Score")
        return None, None
    except Exception as e:
        st.error(f"❌ Unexpected error: {str(e)}")
        return None, None


# Load data - either from upload or default CSV
if uploaded_file is not None:
    # Handle uploaded file
    try:
        import io
        df_temp = pd.read_csv(io.StringIO(uploaded_file.getvalue().decode("utf8")))
        st.sidebar.success(f"✅ Loaded: {uploaded_file.name}")
        
        # Create temporary path for DataEngine
        temp_path = f"data/{uploaded_file.name}"
        df_temp.to_csv(temp_path, index=False)
        data_engine, df = load_data(temp_path)
    except Exception as e:
        st.error(f"❌ Error loading uploaded file: {str(e)}")
        data_engine, df = None, None
else:
    # Use default CSV
    data_engine, df = load_data()

if df is not None:
    # Filter by date range
    df_filtered = data_engine.filter_by_date_range(
        pd.to_datetime(start_date),
        pd.to_datetime(end_date)
    )
    
    # Initialize Analytics Engine
    analytics_engine = AnalyticsEngine(df_filtered)
    
    # ====================================================================
    # DATA VALIDATION & PREVIEW
    # ====================================================================
    
    with st.expander("🔍 Data Preview & Validation", expanded=False):
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Total Records", len(df))
        with col2:
            st.metric("Columns Found", len(df.columns))
        with col3:
            st.metric("Date Range", f"{df['Date'].min().date()} to {df['Date'].max().date()}")
        
        st.markdown("**Columns in your file:**")
        st.code(", ".join(df.columns.tolist()))
        
        st.markdown("**Required columns:**")
        st.code("Date, Provider, Service, Region, Amount, Usage_Type, Efficiency_Score")
        
        # Check for missing columns
        required_cols = ['Date', 'Provider', 'Service', 'Region', 'Amount', 'Usage_Type', 'Efficiency_Score']
        missing_cols = [col for col in required_cols if col not in df.columns]
        
        if missing_cols:
            st.warning(f"⚠️ Missing columns: {', '.join(missing_cols)}")
            st.info("Please ensure your CSV has all required columns with exact names (case-sensitive)")
        else:
            st.success("✅ All required columns found!")
        
        st.markdown("**First few rows:**")
        st.dataframe(df.head(10), use_container_width=True)
    
    st.markdown("---")
    
    # Check if all required columns exist before proceeding
    required_cols = ['Date', 'Provider', 'Service', 'Region', 'Amount', 'Usage_Type', 'Efficiency_Score']
    missing_cols = [col for col in required_cols if col not in df.columns]
    
    if missing_cols:
        st.error(f"❌ Cannot proceed: Missing columns: {', '.join(missing_cols)}")
        st.info("📝 Your CSV must have these exact column names (case-sensitive):\n- Date\n- Provider\n- Service\n- Region\n- Amount\n- Usage_Type\n- Efficiency_Score")
        st.stop()
    
    # Get key metrics
    summary_stats = data_engine.get_summary_statistics()
    mom_stats = analytics_engine.calculate_mom_change()
    unit_econ = analytics_engine.get_unit_economics()
    
    # ========================================================================
    # TAB ORCHESTRATION
    # ========================================================================
    
    tab_descriptive, tab_diagnostic, tab_predictive, tab_prescriptive, tab_connectors = st.tabs([
        "📈 Descriptive Analytics",
        "🔍 Diagnostic Analytics",
        "🔮 Predictive Analytics",
        "💡 Prescriptive Analytics",
        "🔗 Connectors & Integration"
    ])
    
    # ====================================================================
    # TAB 1: DESCRIPTIVE ANALYTICS (KPIs, Overview)
    # ====================================================================
    
    with tab_descriptive:
        st.subheader("Dashboard Overview - Key Performance Indicators")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric(
                label="💰 Total Cloud Spend",
                value=f"${summary_stats['total_spend']:,.2f}",
                delta=f"{mom_stats['mom_change_pct']:.1f}% MoM",
                delta_color="inverse"
            )
        
        with col2:
            st.metric(
                label="📊 Average Monthly Spend",
                value=f"${summary_stats['average_spend']:,.2f}",
                delta="per transaction"
            )
        
        with col3:
            st.metric(
                label="⚡ Avg Efficiency Score",
                value=f"{summary_stats['avg_efficiency']:.1f}/100",
                delta="operational efficiency"
            )
        
        with col4:
            st.metric(
                label="📦 Total Records",
                value=f"{summary_stats['record_count']:,}",
                delta=f"{summary_stats['unique_services']} services"
            )
        
        st.markdown("---")
        
        # Spending breakdown visualizations
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Spend by Cloud Provider")
            spend_by_provider = df_filtered.groupby('Provider')['Amount'].sum().reset_index()
            spend_by_provider = spend_by_provider.sort_values('Amount', ascending=False)
            fig_provider = Visualizer.create_pie_chart(
                spend_by_provider,
                values_col='Amount',
                names_col='Provider'
            )
            st.plotly_chart(fig_provider, use_container_width=True)
        
        with col2:
            st.subheader("Spend by Service")
            spend_by_service = df_filtered.groupby('Service')['Amount'].sum().reset_index()
            spend_by_service = spend_by_service.sort_values('Amount', ascending=False)
            fig_service = Visualizer.create_pie_chart(
                spend_by_service,
                values_col='Amount',
                names_col='Service'
            )
            st.plotly_chart(fig_service, use_container_width=True)
        
        st.markdown("---")
        
        # Time series trend
        st.subheader("Cost Trend Over Selected Period")
        monthly_spend = df_filtered.copy()
        monthly_spend['YearMonth'] = monthly_spend['Date'].dt.to_period('M').astype(str)
        monthly_agg = monthly_spend.groupby('YearMonth')['Amount'].sum().reset_index()
        
        fig_trend = Visualizer.create_time_series(
            monthly_agg,
            x_col='YearMonth',
            y_col='Amount',
            title="Monthly Cloud Spend Trend"
        )
        st.plotly_chart(fig_trend, use_container_width=True)
        
        st.markdown("---")
        
        # Regional heatmap
        st.subheader("Cost Distribution by Region")
        col1, col2 = st.columns(2)
        
        with col1:
            spend_by_region = df_filtered.groupby('Region')['Amount'].sum().reset_index()
            spend_by_region = spend_by_region.sort_values('Amount', ascending=False)
            fig_region = Visualizer.create_bar_chart(
                spend_by_region,
                x_col='Region',
                y_col='Amount',
                title="Total Spend by Region",
                orientation='v'
            )
            st.plotly_chart(fig_region, use_container_width=True)
        
        with col2:
            st.subheader("Usage Type Distribution")
            usage_dist = df_filtered.groupby('Usage_Type')['Amount'].sum().reset_index()
            fig_usage = Visualizer.create_bar_chart(
                usage_dist,
                x_col='Usage_Type',
                y_col='Amount',
                title="Spend by Usage Type"
            )
            st.plotly_chart(fig_usage, use_container_width=True)
    
    # ====================================================================
    # TAB 2: DIAGNOSTIC ANALYTICS (Anomalies, Issues)
    # ====================================================================
    
    with tab_diagnostic:
        st.subheader("Anomaly Detection & Cost Spike Analysis")
        st.markdown(f"**Detecting anomalies with threshold: {anomaly_threshold}% increase**")
        
        # Detect anomalies
        anomalies = analytics_engine.detect_anomalies(threshold_pct=anomaly_threshold)
        
        if not anomalies.empty:
            st.markdown("### 🚨 Detected Cost Anomalies")
            
            # Summary cards for anomalies
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("Total Anomalies", len(anomalies))
            
            with col2:
                critical_count = len(anomalies[anomalies['Severity'] == 'Critical'])
                st.metric("Critical Issues", critical_count, delta_color="inverse")
            
            with col3:
                total_excess = anomalies['Change_Percent'].sum()
                st.metric("Total Excess %", f"{total_excess:.1f}%")
            
            st.markdown("---")
            
            # Anomaly visualization
            fig_anomaly = Visualizer.create_anomaly_highlight(anomalies)
            st.plotly_chart(fig_anomaly, use_container_width=True)
            
            st.markdown("---")
            
            # Detailed anomaly table
            st.subheader("Anomaly Details")
            st.dataframe(
                anomalies[[
                    'Date', 'Service', 'Provider', 'Region',
                    'Baseline_Amount', 'Current_Amount', 'Change_Percent', 'Severity'
                ]].sort_values('Change_Percent', ascending=False),
                use_container_width=True,
                hide_index=True
            )
        
        else:
            st.success("✅ No anomalies detected in the selected period!")
        
        st.markdown("---")
        
        # Low efficiency services
        st.subheader("Low Efficiency Services (< 50 Score)")
        low_efficiency = df_filtered[df_filtered['Efficiency_Score'] < 50].sort_values('Efficiency_Score')
        
        if not low_efficiency.empty:
            st.markdown("#### Services Requiring Optimization")
            fig_efficiency = Visualizer.create_scatter_plot(
                low_efficiency,
                x_col='Amount',
                y_col='Efficiency_Score',
                color_col='Service',
                title="Cost vs Efficiency Score"
            )
            st.plotly_chart(fig_efficiency, use_container_width=True)
            
            # Low efficiency summary
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Services at Risk", low_efficiency['Service'].nunique())
            with col2:
                cost_at_risk = low_efficiency['Amount'].sum()
                st.metric("Cost at Risk", f"${cost_at_risk:,.2f}")
        
        else:
            st.info("✅ All services have good efficiency scores (>= 50)")
    
    # ====================================================================
    # TAB 3: PREDICTIVE ANALYTICS (Forecasting)
    # ====================================================================
    
    with tab_predictive:
        st.subheader("12-Month Cost Forecast & Trend Analysis")
        
        # Generate forecast
        forecast_df = analytics_engine.forecast_spend(periods=forecast_periods)
        
        # Forecast visualization
        fig_forecast = Visualizer.create_forecast_chart(forecast_df)
        st.plotly_chart(fig_forecast, use_container_width=True)
        
        st.markdown("---")
        
        # Forecast metrics
        col1, col2, col3 = st.columns(3)
        
        with col1:
            current_month = forecast_df[forecast_df['Type'] == 'Historical']['Amount'].iloc[-1]
            st.metric("Current Month Spend", f"${current_month:,.2f}")
        
        with col2:
            avg_forecast = forecast_df[forecast_df['Type'] == 'Forecast']['Amount'].mean()
            st.metric("Avg Forecasted Spend", f"${avg_forecast:,.2f}")
        
        with col3:
            last_forecast = forecast_df[forecast_df['Type'] == 'Forecast']['Amount'].iloc[-1]
            pct_change = ((last_forecast - current_month) / current_month * 100)
            st.metric("12-Month Projection", f"${last_forecast:,.2f}",
                     delta=f"{pct_change:.1f}%", delta_color="inverse")
        
        st.markdown("---")
        
        # Cost trend by service forecast
        st.subheader("Cost Trends by Service (Forecast Period)")
        service_trend = analytics_engine.get_cost_trend(groupby_col='Service')
        
        services = service_trend['Service'].unique()
        selected_services = st.multiselect(
            "Select services to analyze",
            services,
            default=services[:3] if len(services) > 0 else []
        )
        
        if selected_services:
            service_filtered = service_trend[service_trend['Service'].isin(selected_services)]
            fig_service_trend = Visualizer.create_time_series(
                service_filtered,
                x_col='YearMonth',
                y_col='Amount',
                color_col='Service',
                title="Service Cost Trends"
            )
            st.plotly_chart(fig_service_trend, use_container_width=True)
    
    # ====================================================================
    # TAB 4: PRESCRIPTIVE ANALYTICS (Recommendations)
    # ====================================================================
    
    with tab_prescriptive:
        st.subheader("Cost Optimization Recommendations")
        
        try:
            # Generate recommendations
            recommendations = analytics_engine.generate_optimization_recommendations()
            
            if not recommendations.empty:
                # Summary metrics
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.metric("Total Recommendations", len(recommendations))
                
                with col2:
                    high_priority = len(recommendations[recommendations['Priority'] == 'High'])
                    st.metric("High Priority", high_priority, delta_color="inverse")
                
                with col3:
                    total_savings = recommendations['Potential_Savings'].sum()
                    st.metric("Total Savings Potential", f"${total_savings:,.2f}")
                
                st.markdown("---")
                
                # Filter by recommendation type
                rec_types = recommendations['Recommendation'].unique().tolist()
                rec_type = st.selectbox(
                    "Filter by Recommendation Type",
                    options=['All'] + rec_types
                )
                
                if rec_type == 'All':
                    filtered_recs = recommendations
                else:
                    filtered_recs = recommendations[recommendations['Recommendation'] == rec_type]
                
                # Display recommendations table
                st.subheader(f"Recommendations ({len(filtered_recs)})")
                st.dataframe(
                    filtered_recs[[
                        'Service', 'Provider', 'Recommendation', 'Current_Spend',
                        'Potential_Savings', 'Priority', 'Efficiency_Score'
                    ]].sort_values('Potential_Savings', ascending=False),
                    use_container_width=True,
                    hide_index=True
                )
                
                st.markdown("---")
                
                # Detailed view
                st.subheader("Optimization Actions")
                for idx, row in filtered_recs.iterrows():
                    with st.expander(f"📌 {row['Service']} - {row['Recommendation']}"):
                        col1, col2 = st.columns(2)
                        with col1:
                            st.write(f"**Provider:** {row['Provider']}")
                            st.write(f"**Current Spend:** ${row['Current_Spend']:,.2f}")
                            st.write(f"**Efficiency Score:** {row['Efficiency_Score']:.1f}")
                        with col2:
                            st.write(f"**Potential Savings:** ${row['Potential_Savings']:,.2f}")
                            st.write(f"**Priority:** {row['Priority']}")
                        st.write(f"**Action:** {row['Action']}")
            
            else:
                st.info("✅ All services are optimized!")
        
        except Exception as e:
            st.error(f"❌ Error generating recommendations: {str(e)}")
            st.info("Please check that your data has all required columns and correct data types.")
    
    # ====================================================================
    # TAB 5: CONNECTORS & INTEGRATION
    # ====================================================================
    
    with tab_connectors:
        st.subheader("Cloud API Connectors & Integration")
        st.markdown("*Connect real-time cost data from AWS, Azure, and other cloud providers*")
        
        st.info(
            "🔧 **Current Status:** Mock/Sample Data Mode  \n"
            "Production integrations can be enabled by configuring API credentials."
        )
        
        # AWS Integration
        with st.expander("☁️ AWS Cost Explorer Integration", expanded=False):
            st.markdown("""
            ### AWS Cost Explorer API
            
            **Setup Instructions:**
            1. Create IAM user with `ce:GetCostAndUsage` permission
            2. Generate Access Key ID and Secret Access Key
            3. Configure AWS credentials in secrets
            
            **Schema Mapping:**
            - AWS Dimension: Service → Service
            - AWS Dimension: Region → Region
            - AWS Metric: Amount → Amount
            - Custom Metadata: Efficiency_Score (calculated from usage patterns)
            
            **Code Example:**
            ```python
            import boto3
            
            ce_client = boto3.client('ce', region_name='us-east-1')
            response = ce_client.get_cost_and_usage(
                TimePeriod={'Start': '2026-01-01', 'End': '2026-02-21'},
                Granularity='DAILY',
                Metrics=['UnblendedCost']
            )
            ```
            """)
        
        # Azure Integration
        with st.expander("☁️ Azure Cost Management Integration", expanded=False):
            st.markdown("""
            ### Azure Cost Management API
            
            **Setup Instructions:**
            1. Register app in Azure AD
            2. Grant "Cost Management Reader" role
            3. Generate client secret
            
            **Schema Mapping:**
            - Subscription → Provider
            - ResourceType → Service
            - ResourceLocation → Region
            - PreTaxCost → Amount
            
            **Code Example:**
            ```python
            from azure.identity import ClientSecretCredential
            from azure.mgmt.costmanagement import CostManagementClient
            
            credentials = ClientSecretCredential(
                client_id='CLIENT_ID',
                client_secret='CLIENT_SECRET',
                tenant_id='TENANT_ID'
            )
            ```
            """)
        
        # GCP Integration
        with st.expander("☁️ Google Cloud Billing Integration", expanded=False):
            st.markdown("""
            ### GCP Big Query Billing Export
            
            **Setup Instructions:**
            1. Enable BigQuery API
            2. Set up billing export to BigQuery
            3. Create service account with BigQuery Reader role
            
            **Schema Mapping:**
            - service.description → Service
            - location.region → Region
            - cost → Amount
            
            **Code Example:**
            ```python
            from google.cloud import bigquery
            
            client = bigquery.Client(project='PROJECT_ID')
            query = '''
            SELECT service.description, location.region, SUM(cost) as amount
            FROM `PROJECT_ID.billing_dataset.gcp_billing_export_v1_*`
            '''
            ```
            """)
        
        # SaaS Connectors
        with st.expander("🔌 SaaS Cost Connectors", expanded=False):
            st.markdown("""
            ### Available SaaS Integrations
            
            | SaaS Provider | Status | Authentication |
            |---------------|--------|-----------------|
            | Databricks | Ready | API Token |
            | Snowflake | Ready | OAuth 2.0 |
            | Fabric (MS) | Ready | AAD Token |
            | Kubernetes | Ready | Kubeconfig |
            | DataDog | Planned | API Key |
            | New Relic | Planned | API Key |
            
            **Custom Connector Template:**
            ```python
            class CustomConnector:
                def __init__(self, api_key):
                    self.api_key = api_key
                
                def fetch_costs(self, start_date, end_date):
                    # Implement API call
                    return normalized_dataframe
            ```
            """)
        
        st.markdown("---")
        
        # Connection Health
        st.subheader("Connection Status")
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("AWS", "⚠️ Demo", help="Using sample data")
        with col2:
            st.metric("Azure", "⚠️ Demo", help="Using sample data")
        with col3:
            st.metric("GCP", "⚠️ Demo", help="Using sample data")
        with col4:
            st.metric("SaaS APIs", "⚠️ Demo", help="Using sample data")
        
        st.info(
            "💡 **Pro Tip:** To enable live integrations, configure API credentials in "
            "`config/secrets.yaml` and set `PRODUCTION_MODE=true` environment variable."
        )

else:
    st.error("❌ Failed to load data. Please check the data file and try again.")
    st.stop()

# ============================================================================
# FOOTER
# ============================================================================

st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #888; padding: 20px;'>
    <small>
    Enterprise FinOps Dashboard v1.0 | 
    Powered by Streamlit, Plotly & Python | 
    © 2026 CloudIQ Analytics
    </small>
</div>
""", unsafe_allow_html=True)
