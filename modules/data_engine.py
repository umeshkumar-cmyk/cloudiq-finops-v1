"""
Data Engine Module - Enterprise FinOps Dashboard
Handles data ingestion, cleaning, and normalization from CSV sources.
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from pathlib import Path


class DataEngine:
    """Enterprise data processing engine for cloud spending data."""
    
    def __init__(self, data_path: str = None):
        """
        Initialize the Data Engine.
        
        Args:
            data_path (str): Path to the CSV file. Defaults to 'data/enterprise_cloud_spend.csv'
        """
        self.data_path = data_path or "data/enterprise_cloud_spend.csv"
        self.df = None
        self.raw_df = None
        
    def load_data(self) -> pd.DataFrame:
        """
        Load and validate cloud spending data from CSV.
        
        Returns:
            pd.DataFrame: Loaded dataframe with validated columns
        """
        try:
            self.raw_df = pd.read_csv(self.data_path)
            self.df = self.raw_df.copy()
            self._validate_schema()
            return self._normalize_data()
        except FileNotFoundError:
            raise FileNotFoundError(f"Data file not found at {self.data_path}")
        except Exception as e:
            raise Exception(f"Error loading data: {str(e)}")
    
    def _validate_schema(self):
        """Validate required columns exist in the dataset."""
        required_columns = ['Date', 'Provider', 'Service', 'Region', 
                           'Amount', 'Usage_Type', 'Efficiency_Score']
        missing = [col for col in required_columns if col not in self.df.columns]
        if missing:
            raise ValueError(f"Missing required columns: {missing}")
    
    def _normalize_data(self) -> pd.DataFrame:
        """
        Normalize and clean the data.
        
        Returns:
            pd.DataFrame: Cleaned and normalized dataframe
        """
        # Convert Date to datetime - handle multiple formats (dd-mm-yyyy, yyyy-mm-dd, etc.)
        try:
            # Try to infer the date format automatically
            self.df['Date'] = pd.to_datetime(self.df['Date'], infer_datetime_format=True, errors='coerce')
        except Exception:
            try:
                # If that fails, try specific format (dd-mm-yyyy)
                self.df['Date'] = pd.to_datetime(self.df['Date'], format='%d-%m-%Y', errors='coerce')
            except Exception:
                # Last resort - try yyyy-mm-dd
                self.df['Date'] = pd.to_datetime(self.df['Date'], format='%Y-%m-%d', errors='coerce')
        
        # Ensure Amount is numeric
        self.df['Amount'] = pd.to_numeric(self.df['Amount'], errors='coerce')
        
        # Ensure Efficiency_Score is numeric (0-100 scale)
        self.df['Efficiency_Score'] = pd.to_numeric(self.df['Efficiency_Score'], errors='coerce')
        
        # Remove rows with missing critical values
        self.df = self.df.dropna(subset=['Date', 'Amount'])
        
        # Sort by date
        self.df = self.df.sort_values('Date').reset_index(drop=True)
        
        return self.df
    
    def get_data(self) -> pd.DataFrame:
        """Get processed dataframe."""
        if self.df is None:
            return self.load_data()
        return self.df
    
    def get_date_range(self) -> tuple:
        """Get min and max dates in dataset."""
        if self.df is None:
            self.load_data()
        return (self.df['Date'].min(), self.df['Date'].max())
    
    def filter_by_date_range(self, start_date: datetime, end_date: datetime) -> pd.DataFrame:
        """
        Filter data by date range.
        
        Args:
            start_date: Start date for filter
            end_date: End date for filter
            
        Returns:
            pd.DataFrame: Filtered dataframe
        """
        if self.df is None:
            self.load_data()
        return self.df[(self.df['Date'] >= start_date) & (self.df['Date'] <= end_date)]
    
    def get_monthly_spend(self) -> pd.DataFrame:
        """
        Aggregate spend by month.
        
        Returns:
            pd.DataFrame: Monthly aggregated spending
        """
        if self.df is None:
            self.load_data()
        
        df_monthly = self.df.copy()
        df_monthly['YearMonth'] = df_monthly['Date'].dt.to_period('M')
        return df_monthly.groupby('YearMonth').agg({
            'Amount': 'sum',
            'Efficiency_Score': 'mean'
        }).reset_index()
    
    def get_spend_by_provider(self) -> pd.DataFrame:
        """Get total spend aggregated by cloud provider."""
        if self.df is None:
            self.load_data()
        return self.df.groupby('Provider').agg({
            'Amount': ['sum', 'mean', 'count'],
            'Efficiency_Score': 'mean'
        }).round(2)
    
    def get_spend_by_service(self) -> pd.DataFrame:
        """Get total spend aggregated by service."""
        if self.df is None:
            self.load_data()
        return self.df.groupby('Service').agg({
            'Amount': ['sum', 'mean', 'count'],
            'Efficiency_Score': 'mean'
        }).round(2)
    
    def get_spend_by_region(self) -> pd.DataFrame:
        """Get total spend aggregated by region."""
        if self.df is None:
            self.load_data()
        return self.df.groupby('Region').agg({
            'Amount': ['sum', 'mean', 'count'],
            'Efficiency_Score': 'mean'
        }).round(2)
    
    def get_efficiency_low_services(self, threshold: float = 50) -> pd.DataFrame:
        """
        Get services with low efficiency scores.
        
        Args:
            threshold: Efficiency score below this value is considered low
            
        Returns:
            pd.DataFrame: Services with low efficiency
        """
        if self.df is None:
            self.load_data()
        return self.df[self.df['Efficiency_Score'] < threshold].sort_values('Efficiency_Score')
    
    def get_high_usage_services(self, threshold: float = 75) -> pd.DataFrame:
        """
        Get services with high usage counts.
        
        Args:
            threshold: Percentile threshold (0-100)
            
        Returns:
            pd.DataFrame: High usage services
        """
        if self.df is None:
            self.load_data()
        amount_threshold = self.df['Amount'].quantile(threshold / 100)
        return self.df[self.df['Amount'] >= amount_threshold].sort_values('Amount', ascending=False)
    
    def get_summary_statistics(self) -> dict:
        """Get overall spending statistics."""
        if self.df is None:
            self.load_data()
        
        return {
            'total_spend': self.df['Amount'].sum(),
            'average_spend': self.df['Amount'].mean(),
            'min_spend': self.df['Amount'].min(),
            'max_spend': self.df['Amount'].max(),
            'std_dev': self.df['Amount'].std(),
            'record_count': len(self.df),
            'unique_providers': self.df['Provider'].nunique(),
            'unique_services': self.df['Service'].nunique(),
            'unique_regions': self.df['Region'].nunique(),
            'avg_efficiency': self.df['Efficiency_Score'].mean(),
        }
