import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans

# فولدر خروجی بسازیم
os.makedirs("output", exist_ok=True)

# داده اصلی
df = pd.read_csv("data/clean/retail_clean.csv")
df['InvoiceDate'] = pd.to_datetime(df['InvoiceDate'])

# تاریخ snapshot = آخرین تاریخ تراکنش
snapshot_date = df['InvoiceDate'].max() + pd.Timedelta(days=1)

# محاسبه RFM
rfm = df.groupby('CustomerID').agg({
    'InvoiceDate': lambda x: (snapshot_date - x.max()).days,
    'InvoiceNo': 'count',
    'TotalPrice': 'sum'
})

rfm.rename(columns={
    'InvoiceDate': 'Recency',
    'InvoiceNo': 'Frequency',
    'TotalPrice': 'Monetary'
}, inplace=True)

# ذخیره RFM اولیه
rfm.to_csv("output/rfm_table.csv", index=True)
print("RFM table saved to output/rfm_table.csv")

############################
#استانداردسازی و خوشه‌بندی با KMeans
############################

# استانداردسازی RFM برای KMeans
scaler = StandardScaler()
rfm_scaled = scaler.fit_transform(rfm)

# خوشه‌بندی
kmeans = KMeans(n_clusters=4, random_state=42)
rfm['Cluster'] = kmeans.fit_predict(rfm_scaled)

# ذخیره جدول خوشه‌بندی
rfm.to_csv("output/rfm_clusters.csv", index=True)
print("RFM clusters saved to output/rfm_clusters.csv")

############################
#نمودار خوشه‌بندی (اختیاری ولی کاربردی برای ارائه)
##############################
plt.figure(figsize=(8,6))
plt.scatter(rfm['Recency'], rfm['Monetary'], c=rfm['Cluster'], cmap='Set2')
plt.xlabel("Recency")
plt.ylabel("Monetary")
plt.title("Customer Segments - RFM Clustering")
plt.colorbar(label="Cluster")
plt.savefig("output/rfm_clusters_plot.png")
plt.show()