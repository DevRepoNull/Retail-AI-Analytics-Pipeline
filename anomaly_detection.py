import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from sklearn.ensemble import IsolationForest

# ============================
# Load data
# ============================

df = pd.read_csv("data/clean/daily_sales.csv")
df["Date"] = pd.to_datetime(df["Date"])
df = df.sort_values("Date")

# ============================
# Feature engineering
# ============================

df["rolling_mean_7"] = df["TotalPrice"].rolling(7).mean()
df["rolling_std_7"] = df["TotalPrice"].rolling(7).std()

df = df.dropna()

features = df[["TotalPrice", "rolling_mean_7", "rolling_std_7"]]

# ============================
# Train Isolation Forest
# ============================

model = IsolationForest(
    n_estimators=200,
    contamination=0.02,
    random_state=42
)

df["anomaly"] = model.fit_predict(features)

# -1 = anomaly
df["is_anomaly"] = df["anomaly"] == -1

# ============================
# Save results
# ============================

os.makedirs("output", exist_ok=True)

df[df["is_anomaly"]].to_csv(
    "output/anomalies.csv",
    index=False
)

# ============================
# Plot
# ============================

plt.figure(figsize=(12, 5))
plt.plot(df["Date"], df["TotalPrice"], label="Sales")

plt.scatter(
    df[df["is_anomaly"]]["Date"],
    df[df["is_anomaly"]]["TotalPrice"],
)

plt.title("Daily Sales Anomaly Detection")
plt.xlabel("Date")
plt.ylabel("Sales")
plt.legend()

plt.tight_layout()
plt.savefig("output/anomaly_plot.png")
plt.close()

print("✅ anomaly_detection.py finished successfully.")
print("📁 output/anomalies.csv saved")
print("📊 output/anomaly_plot.png saved")
