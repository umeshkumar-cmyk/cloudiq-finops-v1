import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

def generate_enterprise_csv():
    providers = {
        'AWS': ['Databricks', 'Snowflake', 'Kubernetes', 'EC2', 'RDS'],
        'Azure': ['Fabric', 'AKS', 'VMs', 'SQL Database'],
        'GCP': ['BigQuery', 'Compute Engine'],
        'SaaS': ['Databricks', 'Snowflake']
    }
    
    data = []
    # Using YYYY-MM-DD for maximum compatibility
    start_date = datetime(2023, 1, 1)
    end_date = datetime(2026, 2, 21)
    
    current_date = start_date
    while current_date <= end_date:
        for _ in range(random.randint(3, 6)):
            provider = random.choice(list(providers.keys()))
            service = random.choice(providers[provider])
            
            data.append({
                'Date': current_date.strftime('%Y-%m-%d'), # CHANGED TO ISO FORMAT
                'Provider': provider,
                'Service': service,
                'Region': 'global',
                'Amount': round(random.uniform(500, 5000), 2),
                'Usage_Type': random.choice(['on-demand', 'reserved']),
                'Efficiency_Score': random.randint(30, 95)
            })
        current_date += timedelta(days=1)

    df = pd.DataFrame(data)
    df.to_csv('enterprise_cloud_spend_3year.csv', index=False)
    print("Success: 'enterprise_cloud_spend_3year.csv' created with YYYY-MM-DD format.")

if __name__ == "__main__":
    generate_enterprise_csv()