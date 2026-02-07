# 🧩 04_clustering.ipynb — خوشه‌بندی مشتریان با RFM

این نوت‌بوک **مشتریان را با استفاده از RFM و KMeans خوشه‌بندی می‌کند** و الگوهای مشتریان کلیدی را شناسایی می‌کند.

---

## 📌 بخش 1 — بارگذاری کتابخانه و داده‌ها

```python
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans

df = pd.read_csv("../data/clean/retail_clean.csv")
```

- pandas / numpy → مدیریت داده

- matplotlib / seaborn → رسم نمودار

- sklearn → استانداردسازی و خوشه‌بندی

- بارگذاری داده تمیز شده

## 📌 بخش 2 — ساخت جدول RFM

```
import datetime as dt

df['InvoiceDate'] = pd.to_datetime(df['InvoiceDate'])
snapshot_date = df['InvoiceDate'].max()

rfm = df.groupby('CustomerID').agg({
    'InvoiceDate': lambda x: (snapshot_date - x.max()).days,
    'InvoiceNo': 'count',
    'TotalPrice': 'sum'
})

rfm.rename(columns={
    'InvoiceDate': 'Recency',
    'InvoiceNo': 'Frequency',
    'TotalPrice': 'MonetaryValue'
}, inplace=True)

print(rfm.head())
```

- Recency → آخرین خرید مشتری (چند روز قبل)

- Frequency → تعداد تراکنش‌ها

- MonetaryValue → مجموع خرید مشتری

- جدول RFM آماده تحلیل و خوشه‌بندی می‌شود

---

## 📌 بخش 3 — استانداردسازی داده‌ها

```
scaler = StandardScaler()
rfm_scaled = scaler.fit_transform(rfm)
```

- استانداردسازی RFM برای KMeans

- جلوگیری از تسلط ستون با مقادیر بزرگتر بر خوشه‌بندی

---

## 📌 بخش 4 — آموزش KMeans

```
kmeans = KMeans(n_clusters=4, random_state=42)
kmeans.fit(rfm_scaled)
rfm['Cluster'] = kmeans.labels_

print(rfm['Cluster'].value_counts())
```

- تعداد خوشه‌ها = ۴ (مثلاً VIP, High, Medium, Low)

- افزودن برچسب خوشه‌ها به جدول RFM

- مشاهده تعداد مشتریان در هر خوشه

---

## 📌 بخش 5 — رسم نمودار خوشه‌ها

```
plt.figure(figsize=(8,5))
sns.scatterplot(
    x='Recency', y='MonetaryValue',
    hue='Cluster', data=rfm, palette='tab10'
)
plt.title("Customer Segmentation")
plt.show()
```

- نمایش مشتریان در فضای Recency vs MonetaryValue

- رنگ‌ها → خوشه‌های KMeans

- بررسی بصری الگوهای مشتریان

---

# ✅ جمع‌بندی

clustering:

- جدول RFM مشتریان را می‌سازد

- داده‌ها را استاندارد می‌کند

- خوشه‌بندی مشتریان با KMeans انجام می‌دهد

- الگوهای مشتریان را بصری می‌کند

- آماده‌سازی داده برای بخش RFM & Clustering در داشبورد Streamlit