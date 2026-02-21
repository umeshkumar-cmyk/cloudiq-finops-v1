"""
Analytics Engine Module - Enterprise FinOps Dashboard
Implements Anomaly Detection, Forecasting, and Optimization recommendations.
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from scipy import stats


class AnalyticsEngine:
    """Advanced analytics for cost optimization and forecasting."""
    
    def __init__(self, dataframe: pd.DataFrame):
        """
        Initialize Analytics Engine with processed data.
        
        Args:
            dataframe (pd.DataFrame): Cleaned data from DataEngine
        """
        self.df = dataframe.copy()
        self.anomalies = None
        self.forecast = None
    
    def detect_anomalies(self, threshold_pct: float = 15.0) -> pd.DataFrame:
        """
        Detect cost anomalies using statistical methods.
        Flags significant positive deviations from baseline.
        
        Args:
            threshold_pct (float): Percentage increase to flag as anomaly (default: 15%)
            
        Returns:
            pd.DataFrame: Anomalies with details
        """
        # Group by Service and calculate daily aggregates
        daily_service = self.df.groupby(['Date', 'Service']).agg({
            'Amount': 'sum',
            'Efficiency_Score': 'mean',
            'Provider': 'first',
            'Region': 'first'
        }).reset_index()
        
        anomalies_list = []
        
        for service in daily_service['Service'].unique():
            service_data = daily_service[daily_service['Service'] == service].sort_values('Date')
            
            if len(service_data) < 3:
                continue
            
            amounts = service_data['Amount'].values
            baseline = np.mean(amounts[:-1])  # Use all but last for baseline
            current = amounts[-1]
            pct_change = ((current - baseline) / baseline * 100) if baseline > 0 else 0
            
            if pct_change > threshold_pct:
                anomalies_list.append({
                    'Date': service_data['Date'].iloc[-1],
                    'Service': service,
                    'Provider': service_data['Provider'].iloc[-1],
                    'Region': service_data['Region'].iloc[-1],
                    'Baseline_Amount': round(baseline, 2),
                    'Current_Amount': round(current, 2),
                    'Change_Percent': round(pct_change, 2),
                    'Severity': 'Critical' if pct_change > 30 else 'High' if pct_change > 20 else 'Medium'
                })
        
        self.anomalies = pd.DataFrame(anomalies_list).sort_values('Change_Percent', ascending=False)
        return self.anomalies
    
    def forecast_spend(self, periods: int = 12, poly_degree: int = 2) -> pd.DataFrame:
        """
        Forecast cloud spending using polynomial regression.
        
        Args:
            periods (int): Number of months to forecast
            poly_degree (int): Degree of polynomial (1=linear, 2=quadratic, etc.)
            
        Returns:
            pd.DataFrame: Historical data + forecast
        """
        # Aggregate to monthly level
        monthly = self.df.copy()
        monthly['YearMonth'] = monthly['Date'].dt.to_period('M').astype(str)
        monthly_spend = monthly.groupby('YearMonth')['Amount'].sum().reset_index()
        monthly_spend['MonthIndex'] = range(len(monthly_spend))
        
        # Prepare for polynomial regression
        X = monthly_spend['MonthIndex'].values.reshape(-1, 1)
        y = monthly_spend['Amount'].values
        
        # Fit polynomial
        coefficients = np.polyfit(X.flatten(), y, poly_degree)
        poly_func = np.poly1d(coefficients)
        
        # Generate forecast
        last_month_idx = X.flatten()[-1]
        future_indices = np.arange(last_month_idx + 1, last_month_idx + periods + 1)
        forecast_values = poly_func(future_indices)
        
        # Create forecast dataframe
        last_date = pd.to_datetime(monthly_spend['YearMonth'].iloc[-1])
        forecast_dates = [last_date + timedelta(days=30*i) for i in range(1, periods + 1)]
        forecast_dates = [d.strftime('%Y-%m') for d in forecast_dates]
        
        forecast_df = pd.DataFrame({
            'YearMonth': forecast_dates,
            'Amount': forecast_values,
            'Type': 'Forecast'
        })
        
        # Combine historical + forecast
        historical = monthly_spend[['YearMonth', 'Amount']].copy()
        historical['Type'] = 'Historical'
        
        self.forecast = pd.concat([historical, forecast_df], ignore_index=True)
        return self.forecast
    
    def get_anomalies(self) -> pd.DataFrame:
        """Get detected anomalies (runs detect_anomalies if not already run)."""
        if self.anomalies is None:
            return self.detect_anomalies()
        return self.anomalies
    
    def generate_optimization_recommendations(self, efficiency_threshold: float = 50) -> pd.DataFrame:
        """
        Generate optimization recommendations based on efficiency scores.
        
        Args:
            efficiency_threshold (float): Score below this triggers recommendation
            
        Returns:
            pd.DataFrame: Optimization recommendations
        """
        recommendations = []
        
        try:
            # Group by Service and Provider
            service_stats = self.df.groupby(['Service', 'Provider']).agg({
                'Amount': ['sum', 'count', 'mean'],
                'Efficiency_Score': 'mean',
                'Usage_Type': lambda x: x.mode()[0] if len(x.mode()) > 0 else 'Unknown'
            }).reset_index()
            
            service_stats.columns = ['Service', 'Provider', 'Total_Amount', 'Usage_Count', 
                                     'Avg_Amount', 'Avg_Efficiency', 'Primary_Usage']
            
            for idx, row in service_stats.iterrows():
                rec_type = None
                rec_action = None
                savings_potential = 0.0
                
                # Convert to numeric to ensure calculations work
                avg_efficiency = float(row['Avg_Efficiency']) if pd.notna(row['Avg_Efficiency']) else 100
                usage_count = int(row['Usage_Count']) if pd.notna(row['Usage_Count']) else 0
                total_amount = float(row['Total_Amount']) if pd.notna(row['Total_Amount']) else 0
                
                # Low efficiency = Rightsizing
                if avg_efficiency < efficiency_threshold:
                    rec_type = 'Rightsizing'
                    rec_action = f"Analyze {row['Service']} resource allocation, consolidate underutilized instances"
                    savings_potential = total_amount * 0.2  # Assume 20% potential savings
                
                # High consistent usage = Reserved Instances
                elif usage_count > 50 and avg_efficiency >= 75:
                    rec_type = 'Reserved Instances'
                    rec_action = f"Purchase Reserved Instances for {row['Service']} to lock in costs"
                    savings_potential = total_amount * 0.25  # Assume 25% savings from RIs
                
                # Idle resources = Cleanup
                elif usage_count < 10 and total_amount > 100:
                    rec_type = 'Resource Cleanup'
                    rec_action = f"Terminate unused {row['Service']} instances in {row['Provider']}"
                    savings_potential = total_amount * 0.15
                
                if rec_type:
                    recommendations.append({
                        'Service': str(row['Service']),
                        'Provider': str(row['Provider']),
                        'Recommendation': rec_type,
                        'Action': rec_action,
                        'Current_Spend': float(round(total_amount, 2)),
                        'Potential_Savings': float(round(savings_potential, 2)),
                        'Priority': 'High' if savings_potential > total_amount * 0.2 else 'Medium',
                        'Efficiency_Score': float(round(avg_efficiency, 1))
                    })
            
            if recommendations:
                return pd.DataFrame(recommendations).sort_values('Potential_Savings', ascending=False)
            else:
                # Return empty dataframe with correct columns
                return pd.DataFrame(columns=[
                    'Service', 'Provider', 'Recommendation', 'Action', 
                    'Current_Spend', 'Potential_Savings', 'Priority', 'Efficiency_Score'
                ])
        
        except Exception as e:
            # Return empty dataframe if error occurs
            print(f"Error generating recommendations: {str(e)}")
            return pd.DataFrame(columns=[
                'Service', 'Provider', 'Recommendation', 'Action', 
                'Current_Spend', 'Potential_Savings', 'Priority', 'Efficiency_Score'
            ])
    
    def get_cost_trend(self, groupby_col: str = 'Service') -> pd.DataFrame:
        """
        Get cost trends over time for a specific dimension.
        
        Args:
            groupby_col (str): Column to group by ('Service', 'Provider', 'Region')
            
        Returns:
            pd.DataFrame: Trend data
        """
        trend = self.df.copy()
        trend['YearMonth'] = trend['Date'].dt.to_period('M').astype(str)
        return trend.groupby(['YearMonth', groupby_col])['Amount'].sum().reset_index()
    
    def calculate_mom_change(self) -> dict:
        """
        Calculate Month-over-Month change in total spend.
        
        Returns:
            dict: MoM metrics
        """
        monthly = self.df.copy()
        monthly['YearMonth'] = monthly['Date'].dt.to_period('M').astype(str)
        monthly_spend = monthly.groupby('YearMonth')['Amount'].sum()
        
        if len(monthly_spend) < 2:
            return {'current_month': 0, 'previous_month': 0, 'mom_change': 0, 'mom_change_pct': 0}
        
        current = monthly_spend.iloc[-1]
        previous = monthly_spend.iloc[-2]
        change = current - previous
        change_pct = (change / previous * 100) if previous > 0 else 0
        
        return {
            'current_month': round(current, 2),
            'previous_month': round(previous, 2),
            'mom_change': round(change, 2),
            'mom_change_pct': round(change_pct, 2)
        }
    
    def get_unit_economics(self) -> dict:
        """
        Calculate unit economics metrics.
        
        Returns:
            dict: Unit economics data
        """
        return {
            'cost_per_unit': round(self.df.groupby('Service')['Amount'].mean().mean(), 2),
            'avg_efficiency_cost_ratio': round(
                self.df['Amount'].sum() / (self.df['Efficiency_Score'].mean() + 0.001), 2
            ),
            'total_units': len(self.df),
            'avg_spend_per_transaction': round(self.df['Amount'].mean(), 2)
        }
