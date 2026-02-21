"""
CloudIQ FinOps Dashboard - Analytics Module Package

A professional-grade financial operations analytics platform with:
- Descriptive Analytics: Historical cost analysis
- Diagnostic Analytics: Anomaly detection & root cause analysis
- Predictive Analytics: 12-month cost forecasting
- Prescriptive Analytics: Optimization recommendations
"""

from .data_engine import DataEngine
from .analytics_engine import AnalyticsEngine
from .visualizer import Visualizer

__version__ = "1.0.0"
__author__ = "CloudIQ Analytics Team"
__all__ = ["DataEngine", "AnalyticsEngine", "Visualizer"]
