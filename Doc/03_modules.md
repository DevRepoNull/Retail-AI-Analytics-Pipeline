# 🧩 ماژول‌ها و نقش آن‌ها

---

## 📥 fetch_data.py

🎯 دانلود دیتاست از Kaggle  
📦 ذخیره در data/raw

---

## 🧼 clean_data.py

- حذف NaN
- حذف فاکتورهای منفی
- ساخت TotalPrice
- تجمیع روزانه فروش

خروجی: daily_sales.csv

---

## 📊 analysis.py

- توزیع فروش
- آموزش Linear Regression
- Random Forest
- محاسبه MAE و RMSE
- ذخیره نمودارها

---

## 📈 forecasting.py

- ساخت lag features
- rolling mean
- آموزش مدل
- پیش‌بینی فروش آینده

---

## 👥 rfm_analysis.py

- Recency
- Frequency
- Monetary
- KMeans Clustering

---

## 🚨 anomaly_detection.py

- IsolationForest
- تشخیص فروش غیرعادی
- رسم نمودار

---

## 🌐 app.py

داشبورد Streamlit شامل:

- Overview
- Analysis
- Forecasting
- RFM
- Anomaly
