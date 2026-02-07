# 🔍 02_eda.ipynb — تحلیل اکتشافی داده‌ها (EDA)

این نوت‌بوک **تحلیل اکتشافی داده‌های فروش** را انجام می‌دهد و روندها و الگوها را بصری می‌کند.

---

## 📌 بخش 1 — بارگذاری کتابخانه و داده‌ها

```python
import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("../data/clean/retail_clean.csv")
daily = pd.read_csv("../data/clean/daily_sales.csv")

print(df.head())
print(df.shape)
```

- pandas → مدیریت داده‌ها

- matplotlib → رسم نمودارها

- بارگذاری داده تمیز شده (retail_clean.csv) و فروش روزانه (daily_sales.csv)

- نمایش چند رکورد اول و ابعاد داده

---

## 📌 بخش 2 — نمودار فروش روزانه

```
daily["Date"] = pd.to_datetime(daily["Date"])

plt.figure(figsize=(12,5))
plt.plot(daily["Date"], daily["TotalPrice"])
plt.title("Daily Total Sales")
plt.xlabel("Date")
plt.ylabel("Sales")
plt.show()
```

- ستون تاریخ به datetime تبدیل شد

- رسم روند فروش روزانه

- شناسایی الگوها و نوسانات کوتاه‌مدت

---

## 📌 بخش 3 — روند ماهانه فروش

```
daily["Month"] = daily["Date"].dt.to_period("M").astype(str)
monthly = daily.groupby("Month")["TotalPrice"].sum()

plt.figure(figsize=(12,5))
monthly.plot()
plt.title("Monthly Sales Trend")
plt.xlabel("Month")
plt.ylabel("Sales")
plt.xticks(rotation=45)
plt.show()
```

- جمع فروش ماهانه

- رسم trend ماهانه برای شناسایی فصلی بودن فروش

---

## 📌 بخش 4 — 10 کشور برتر بر اساس درآمد

```
top_countries = df.groupby("Country")["TotalPrice"].sum().sort_values(ascending=False).head(10)

plt.figure(figsize=(10,5))
top_countries.plot(kind="bar")
plt.title("Top 10 Countries by Revenue")
plt.ylabel("Revenue")
plt.show()
```

- کشورها بر اساس مجموع فروش مرتب شدند

- نمایش بار نمودار کشورها با بیشترین درآمد

---

## 📌 بخش 5 — 10 محصول برتر بر اساس درآمد

```
top_products = df.groupby("StockCode")["TotalPrice"].sum().sort_values(ascending=False).head(10)

plt.figure(figsize=(10,5))
top_products.plot(kind="bar")
plt.title("Top 10 Products by Revenue")
plt.ylabel("Revenue")
plt.show()
```

- محصولات پرفروش بر اساس مجموع فروش

- شناسایی محصولات کلیدی برای استراتژی بازاریابی

---

## 📌 بخش 6 — توزیع کل فاکتورها

```
invoice_totals = df.groupby("InvoiceNo")["TotalPrice"].sum()

plt.figure(figsize=(8,5))
plt.hist(invoice_totals, bins=50)
plt.title("Distribution of Invoice Total")
plt.xlabel("Invoice Amount")
plt.ylabel("Frequency")
plt.show()
```

- بررسی توزیع مبلغ فاکتورها

- شناسایی outlier‌ها و تراکنش‌های غیرمعمول

---

✅ جمع‌بندی

eda:

- روندهای روزانه و ماهانه فروش را تحلیل می‌کند

- درآمد کشورها و محصولات را نمایش می‌دهد

- توزیع فاکتورها را برای شناسایی الگو و ناهنجاری بررسی می‌کند

- آماده‌سازی پایه برای پیش‌بینی و خوشه‌بندی مشتریان
