import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor, IsolationForest
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_absolute_error, mean_squared_error
from sklearn.cluster import KMeans

import os

# اگر فولدر وجود ندارد، بسازش
os.makedirs("output", exist_ok=True)

# -------------------------
# Load cleaned data
# -------------------------
df = pd.read_csv("data/clean/retail_clean.csv")
df['InvoiceDate'] = pd.to_datetime(df['InvoiceDate'])

# -------------------------
# EDA: Distribution of Invoice Total
# -------------------------
invoice_totals = df.groupby("InvoiceNo")["TotalPrice"].sum()
plt.figure(figsize=(8,5))
plt.hist(invoice_totals, bins=50)
plt.title("Distribution of Invoice Total")
plt.xlabel("Invoice Amount")
plt.ylabel("Frequency")
plt.savefig("output/invoice_total_distribution.png")
plt.close()

# -------------------------
# Forecasting: Linear + Random Forest
# -------------------------
# Example: aggregate daily sales
daily_sales = df.groupby(df['InvoiceDate'].dt.date)['TotalPrice'].sum().reset_index()
daily_sales.columns = ['Date', 'Sales']

# train/test split
train = daily_sales.iloc[:-30]
test = daily_sales.iloc[-30:]
X_train = np.arange(len(train)).reshape(-1,1)
y_train = train['Sales'].values
X_test = np.arange(len(train), len(train)+len(test)).reshape(-1,1)
y_test = test['Sales'].values

# Linear Regression
lr = LinearRegression()
lr.fit(X_train, y_train)
pred_lr = lr.predict(X_test)
print("Linear MAE:", mean_absolute_error(y_test, pred_lr))
print("Linear RMSE:", np.sqrt(mean_squared_error(y_test, pred_lr)))

# Random Forest
rf = RandomForestRegressor(n_estimators=200, random_state=42)
rf.fit(X_train, y_train)
pred_rf = rf.predict(X_test)
print("RF MAE:", mean_absolute_error(y_test, pred_rf))
print("RF RMSE:", np.sqrt(mean_squared_error(y_test, pred_rf)))

# Save forecast
forecast_df = pd.DataFrame({'Date': test['Date'], 'Actual': y_test, 'Predicted_RF': pred_rf})
forecast_df.to_csv("output/sales_forecast.csv", index=False)

# -------------------------
# Clustering: RFM + KMeans
# -------------------------
snapshot_date = df['InvoiceDate'].max()
rfm = df.groupby('CustomerID').agg({
    'InvoiceDate': lambda x: (snapshot_date - x.max()).days,
    'InvoiceNo': 'count',
    'TotalPrice': 'sum'
})
rfm.rename(columns={'InvoiceDate':'Recency','InvoiceNo':'Frequency','TotalPrice':'MonetaryValue'}, inplace=True)
scaler = StandardScaler()
rfm_scaled = scaler.fit_transform(rfm)
kmeans = KMeans(n_clusters=4, random_state=42)
kmeans.fit(rfm_scaled)
rfm['Cluster'] = kmeans.labels_
rfm.to_csv("output/customer_clusters.csv", index=True)

# -------------------------
# Anomaly Detection
# -------------------------
X = df[['Quantity', 'TotalPrice']]
iso_forest = IsolationForest(n_estimators=200, contamination=0.01, random_state=42)
iso_forest.fit(X)
df['Anomaly'] = iso_forest.predict(X)
df[df['Anomaly']==-1].to_csv("output/anomalies.csv", index=False)
