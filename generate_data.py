import pandas as pd
import numpy as np
from datetime import datetime

np.random.seed(42)

# Generate 30 days of normal sensor data
dates = pd.date_range('2024-11-01', '2024-11-30', freq='10min')
n = len(dates)

# Normal operation
data = {
    'timestamp': dates,
    'temperature': np.random.normal(24, 2, n),
    'humidity': np.random.normal(55, 8, n),
    'pressure': np.random.normal(1013, 5, n)
}

df_normal = pd.DataFrame(data)
df_normal['anomaly'] = 0 # Label: 0 = normal

# Inject anomalies (5% of data)
n_anomalies = int(0.05 * n)
anomaly_indices = np.random.choice(df_normal.index, n_anomalies, replace=False)

for idx in anomaly_indices:
    # Random anomaly type
    anomaly_type = np.random.choice(['spike', 'drift', 'stuck'])

    if anomaly_type == 'spike':
        # Sudden spike
        df_normal.loc[idx, 'temperature'] += np.random.uniform(10, 20)
    elif anomaly_type == 'drift':
        # Gradual drift
        df_normal.loc[idx:idx+10, 'humidity'] += np.linspace(0, 30, 11)
    else: # Stuck
        # Sensor stuck at value
        df_normal.loc[idx:idx+5, 'pressure'] = df_normal.loc[idx, 'pressure']

    df_normal.loc[idx, 'anomaly'] = 1 # Label anomaly

# Save
df_normal.to_csv('sensor_data.csv', index=False)
print(f"Generated {len(df_normal)} samples")
print(f"Anomalies: {df_normal['anomaly'].sum()} ({df_normal['anomaly'].mean()*100:.1f}%)")