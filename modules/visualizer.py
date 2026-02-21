"""
Visualizer Module - Enterprise FinOps Dashboard
Creates Plotly charts with Dark Mode theme for professional visualization.
"""

import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots


# Dark mode color scheme
DARK_TEMPLATE = "plotly_dark"
PRIMARY_COLOR = "#00D9FF"  # Cyan
SECONDARY_COLOR = "#FF6B6B"  # Red (for alerts)
SUCCESS_COLOR = "#51CF66"  # Green
WARNING_COLOR = "#FFD93D"  # Yellow


class Visualizer:
    """Professional data visualization engine for FinOps metrics."""
    
    @staticmethod
    def create_kpi_card(title: str, value: str, metric: str, delta: float = None) -> go.Figure:
        """
        Create a KPI card visualization.
        
        Args:
            title (str): Card title
            value (str): Main value to display
            metric (str): Metric unit/description
            delta (float): Optional percentage change
            
        Returns:
            go.Figure: Plotly figure
        """
        fig = go.Figure(go.Indicator(
            mode="number+gauge",
            value=float(value.replace('$', '').replace(',', '')) if isinstance(value, str) else value,
            title={'text': title},
            domain={'x': [0, 1], 'y': [0, 1]}
        ))
        
        fig.update_layout(
            template=DARK_TEMPLATE,
            height=300,
            font=dict(size=14, color="white"),
            margin=dict(l=10, r=10, t=30, b=10),
            paper_bgcolor="rgba(20, 33, 61, 0.8)",
            plot_bgcolor="rgba(20, 33, 61, 0.8)"
        )
        
        return fig
    
    @staticmethod
    def create_time_series(df: pd.DataFrame, x_col: str = 'Date', y_col: str = 'Amount',
                          title: str = "Cost Trend Over Time", color_col: str = None) -> go.Figure:
        """
        Create a time series line chart.
        
        Args:
            df (pd.DataFrame): Data to plot
            x_col (str): X-axis column
            y_col (str): Y-axis column
            title (str): Chart title
            color_col (str): Optional column for line colors
            
        Returns:
            go.Figure: Plotly figure
        """
        if color_col:
            fig = px.line(df, x=x_col, y=y_col, color=color_col, 
                         title=title, markers=True)
        else:
            fig = px.line(df, x=x_col, y=y_col, title=title, markers=True)
        
        fig.update_traces(line=dict(width=2.5))
        fig.update_layout(
            template=DARK_TEMPLATE,
            height=400,
            hovermode='x unified',
            title_font_size=16,
            font=dict(size=12, color="white"),
            xaxis_title_font_size=12,
            yaxis_title_font_size=12,
            paper_bgcolor="rgba(20, 33, 61, 0.8)",
            plot_bgcolor="rgba(20, 33, 61, 0.8)"
        )
        
        return fig
    
    @staticmethod
    def create_bar_chart(df: pd.DataFrame, x_col: str, y_col: str, 
                        title: str = "Cost Breakdown", orientation: str = 'v',
                        color: str = PRIMARY_COLOR) -> go.Figure:
        """
        Create a bar chart.
        
        Args:
            df (pd.DataFrame): Data to plot
            x_col (str): X-axis column
            y_col (str): Y-axis column
            title (str): Chart title
            orientation (str): 'v' for vertical, 'h' for horizontal
            color (str): Bar color
            
        Returns:
            go.Figure: Plotly figure
        """
        fig = px.bar(df, x=x_col, y=y_col, title=title, 
                    orientation=orientation, text_auto='.2f')
        
        fig.update_traces(marker_color=color)
        fig.update_layout(
            template=DARK_TEMPLATE,
            height=400,
            title_font_size=16,
            font=dict(size=11, color="white"),
            paper_bgcolor="rgba(20, 33, 61, 0.8)",
            plot_bgcolor="rgba(20, 33, 61, 0.8)",
            xaxis_title_font_size=12,
            yaxis_title_font_size=12
        )
        
        return fig
    
    @staticmethod
    def create_pie_chart(df: pd.DataFrame, values_col: str, names_col: str,
                        title: str = "Cost Distribution") -> go.Figure:
        """
        Create a pie chart.
        
        Args:
            df (pd.DataFrame): Data to plot
            values_col (str): Values column
            names_col (str): Names/labels column
            title (str): Chart title
            
        Returns:
            go.Figure: Plotly figure
        """
        fig = px.pie(df, values=values_col, names=names_col, title=title)
        
        fig.update_layout(
            template=DARK_TEMPLATE,
            height=400,
            title_font_size=16,
            font=dict(size=12, color="white"),
            paper_bgcolor="rgba(20, 33, 61, 0.8)",
            plot_bgcolor="rgba(20, 33, 61, 0.8)"
        )
        
        return fig
    
    @staticmethod
    def create_scatter_plot(df: pd.DataFrame, x_col: str, y_col: str, 
                           title: str = "Cost vs Efficiency", size_col: str = None,
                           color_col: str = None) -> go.Figure:
        """
        Create a scatter plot.
        
        Args:
            df (pd.DataFrame): Data to plot
            x_col (str): X-axis column
            y_col (str): Y-axis column
            title (str): Chart title
            size_col (str): Optional column for bubble size
            color_col (str): Optional column for colors
            
        Returns:
            go.Figure: Plotly figure
        """
        fig = px.scatter(df, x=x_col, y=y_col, size=size_col, 
                        color=color_col, title=title, opacity=0.7)
        
        fig.update_layout(
            template=DARK_TEMPLATE,
            height=400,
            title_font_size=16,
            font=dict(size=12, color="white"),
            paper_bgcolor="rgba(20, 33, 61, 0.8)",
            plot_bgcolor="rgba(20, 33, 61, 0.8)"
        )
        
        return fig
    
    @staticmethod
    def create_forecast_chart(historical_df: pd.DataFrame, forecast_df: pd.DataFrame = None,
                             title: str = "12-Month Cost Forecast") -> go.Figure:
        """
        Create a forecast visualization with historical and predicted values.
        
        Args:
            historical_df (pd.DataFrame): Historical data with columns [YearMonth, Amount, Type]
            forecast_df (pd.DataFrame): Forecast data (optional, can be in same df)
            title (str): Chart title
            
        Returns:
            go.Figure: Plotly figure
        """
        combined_df = historical_df if forecast_df is None else pd.concat([historical_df, forecast_df])
        
        fig = go.Figure()
        
        # Historical line
        hist = combined_df[combined_df['Type'] == 'Historical']
        fig.add_trace(go.Scatter(
            x=hist['YearMonth'], y=hist['Amount'],
            mode='lines+markers',
            name='Historical',
            line=dict(color=PRIMARY_COLOR, width=3),
            marker=dict(size=8)
        ))
        
        # Forecast line
        fcst = combined_df[combined_df['Type'] == 'Forecast']
        fig.add_trace(go.Scatter(
            x=fcst['YearMonth'], y=fcst['Amount'],
            mode='lines+markers',
            name='Forecast',
            line=dict(color=WARNING_COLOR, width=3, dash='dash'),
            marker=dict(size=8)
        ))
        
        fig.update_layout(
            title=title,
            template=DARK_TEMPLATE,
            height=400,
            hovermode='x unified',
            title_font_size=16,
            font=dict(size=12, color="white"),
            legend=dict(font=dict(size=11)),
            paper_bgcolor="rgba(20, 33, 61, 0.8)",
            plot_bgcolor="rgba(20, 33, 61, 0.8)",
            xaxis_title="Period",
            yaxis_title="Amount ($)"
        )
        
        return fig
    
    @staticmethod
    def create_anomaly_highlight(anomalies_df: pd.DataFrame) -> go.Figure:
        """
        Create a visualization highlighting detected anomalies.
        
        Args:
            anomalies_df (pd.DataFrame): Anomalies data
            
        Returns:
            go.Figure: Plotly figure
        """
        if anomalies_df.empty:
            fig = go.Figure()
            fig.add_annotation(text="No anomalies detected in current period",
                             x=0.5, y=0.5, showarrow=False)
            return fig
        
        # Create color map for severity
        color_map = {'Critical': SECONDARY_COLOR, 'High': WARNING_COLOR, 'Medium': PRIMARY_COLOR}
        anomalies_df['Color'] = anomalies_df['Severity'].map(color_map)
        
        fig = px.bar(anomalies_df, x='Service', y='Change_Percent',
                    color='Severity', title='Detected Cost Anomalies',
                    hover_data=['Provider', 'Region', 'Current_Amount'],
                    color_discrete_map={'Critical': SECONDARY_COLOR, 
                                       'High': WARNING_COLOR, 
                                       'Medium': PRIMARY_COLOR})
        
        fig.update_layout(
            template=DARK_TEMPLATE,
            height=400,
            title_font_size=16,
            font=dict(size=12, color="white"),
            paper_bgcolor="rgba(20, 33, 61, 0.8)",
            plot_bgcolor="rgba(20, 33, 61, 0.8)",
            xaxis_title="Service",
            yaxis_title="Change %"
        )
        
        return fig
    
    @staticmethod
    def create_heatmap(df: pd.DataFrame, x_col: str, y_col: str, z_col: str,
                      title: str = "Cost Heatmap") -> go.Figure:
        """
        Create a heatmap visualization.
        
        Args:
            df (pd.DataFrame): Data to plot
            x_col (str): X-axis column
            y_col (str): Y-axis column
            z_col (str): Values column (will be color intensity)
            title (str): Chart title
            
        Returns:
            go.Figure: Plotly figure
        """
        pivot_df = df.pivot_table(values=z_col, index=y_col, columns=x_col, aggfunc='sum')
        
        fig = go.Figure(data=go.Heatmap(
            z=pivot_df.values,
            x=pivot_df.columns,
            y=pivot_df.index,
            colorscale='Viridis',
            colorbar=dict(title="Amount ($)")
        ))
        
        fig.update_layout(
            title=title,
            template=DARK_TEMPLATE,
            height=400,
            title_font_size=16,
            font=dict(size=12, color="white"),
            paper_bgcolor="rgba(20, 33, 61, 0.8)",
            plot_bgcolor="rgba(20, 33, 61, 0.8)"
        )
        
        return fig
