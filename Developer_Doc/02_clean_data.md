# 🧼 clean_data.py — پاک‌سازی و آماده‌سازی داده‌ها

این ماژول داده‌ی خام دانلودشده از Kaggle را پردازش می‌کند و دو خروجی اصلی می‌سازد:

1️⃣ داده‌ی تراکنشی تمیز  
2️⃣ فروش روزانه‌ی تجمیع‌شده برای مدل‌های سری زمانی  

---

# 🎯 هدف این فایل چیست؟

کارهای اصلی `clean_data.py`:

✔️ پیدا کردن فایل CSV خام  
✔️ حذف رکوردهای ناقص  
✔️ حذف بازگشت کالا (Quantity منفی)  
✔️ حذف قیمت‌های نامعتبر  
✔️ تبدیل تاریخ‌ها  
✔️ ساخت ستون TotalPrice  
✔️ ذخیره داده‌ی تمیز  
✔️ ساخت دیتاست روزانه فروش  

این فایل پلی است بین **Raw Data** و **Model-ready Data**.

---

# 🧭 جایگاه در Pipeline

data/raw/
↓
clean_data.py
↓
data/clean/
├── retail_clean.csv
└── daily_sales.csv

---

# 📄 کد کامل

```python
import pandas as pd
import os

RAW_DIR = "data/raw"
CLEAN_DIR = "data/clean"

os.makedirs(CLEAN_DIR, exist_ok=True)

def find_csv_file():
    for f in os.listdir(RAW_DIR):
        if f.lower().endswith(".csv"):
            return os.path.join(RAW_DIR, f)
    raise FileNotFoundError("No CSV file found in data/raw")

def clean_data():
    path = find_csv_file()
    print("Loading:", path)

    df = pd.read_csv(path, encoding="ISO-8859-1")

    print("Orginal shape:", df.shape)

    #Drop missing customers
    df = df.dropna(subset=["CustomerID"])

    #Remove returns / negative quantities
    df = df[df["Quantity"] > 0]

    #Remove zero or negative prices
    df = df[df["UnitPrice"] > 0]
    
    #Convert date
    df["InvoiceDate"] = pd.to_datetime(df["InvoiceDate"])

    #Total price per row
    df["TotalPrice"] = df["Quantity"] * df["UnitPrice"]

    print("After cleaning:", df.shape)

    clean_path = os.path.join(CLEAN_DIR, "retail_clean.csv")
    df.to_csv(clean_path, index=False)

    print("Saved cleaned data to:", clean_path)

    #Daily aggregated sales
    df["Date"] = df["InvoiceDate"].dt.date
    daily = df.groupby("Date")["TotalPrice"].sum().reset_index()

    daily_path = os.path.join(CLEAN_DIR, "daily_sales.csv")
    daily.to_csv(daily_path, index=False)

    print("Saved daily sales to:", daily_path)

if __name__ == "__main__":
    clean_data()
```
---

# 🔍 توضیح خط‌به‌خط کد

---

## 📦 import pandas as pd

کتابخانه‌ی اصلی برای:

- خواندن CSV

- فیلتر کردن داده‌ها

- ساخت ستون جدید

- groupby و aggregation

---

## 📦 import os

برای کار با فولدرها و فایل‌ها.

---

## 📁 تعریف مسیرها

```
RAW_DIR = "data/raw"
CLEAN_DIR = "data/clean"
```
تمام مسیرها ثابت و استاندارد هستند.

---

## 🏗️ ساخت فولدر خروجی

```
os.makedirs(CLEAN_DIR, exist_ok=True)
```
اگر پوشه وجود نداشت → ساخته می‌شود.

---

## 🔎 تابع find_csv_file()

این تابع داخل data/raw می‌گردد و اولین فایل CSV را پیدا می‌کند.

اگر هیچ CSV وجود نداشت → خطا می‌دهد.

این طراحی باعث می‌شود pipeline fail-fast باشد.

---

## 📥 بارگذاری داده

```
df = pd.read_csv(path, encoding="ISO-8859-1")
```

Encoding مخصوص دیتاست Online Retail است.

بدون این پارامتر احتمال خطای Unicode وجود دارد.

---

📐 چاپ ابعاد اولیه

```
print("Orginal shape:", df.shape)
```
برای debugging و گزارش اولیه کیفیت داده.

---

🧹 حذف CustomerID خالی

```
df = df[df["Quantity"] > 0]
```
تراکنش‌های بازگشت کالا حذف می‌شوند.

---

## 💲 حذف قیمت‌های غیرمنطقی

```
df = df[df["UnitPrice"] > 0]
```

قیمت صفر یا منفی برای تحلیل فروش معتبر نیست.

---

## 📅 تبدیل تاریخ

```
df["InvoiceDate"] = pd.to_datetime(df["InvoiceDate"])
```

ضروری برای:

- سری زمانی

- استخراج روز

- مرتب‌سازی زمانی

---

## 🧮 ساخت TotalPrice

```
df["TotalPrice"] = df["Quantity"] * df["UnitPrice"]
```

مهم‌ترین ستون مالی پروژه.

---

## 📤 ذخیره داده‌ی تمیز

```
df.to_csv(clean_path, index=False)
```

خروجی تراکنشی کامل.

---

## 📊 ساخت فروش روزانه

```
df["Date"] = df["InvoiceDate"].dt.date
daily = df.groupby("Date")["TotalPrice"].sum().reset_index()
```

این دیتاست ورودی اصلی forecasting است.

---

## 💾 ذخیره daily_sales.csv

```
daily.to_csv(daily_path, index=False)
```

---

## 📤 ورودی‌ها و خروجی‌ها

📥 ورودی

- فایل CSV خام در data/raw/

📤 خروجی

در data/clean/:

- retail_clean.csv

- daily_sales.csv

---

## 🧠 نکات طراحی مهندسی

این فایل:

✔️ idempotent است
✔️ فولدرها را خودکار می‌سازد
✔️ داده‌ی مدل‌پذیر تولید می‌کند
✔️ جداگانه daily dataset می‌دهد

در نسخه پیشرفته‌تر می‌شود افزود:

- schema validation

- logging

- گزارش درصد حذف داده

- config.yaml

- CLI arguments

---

## ✅ جمع‌بندی این ماژول

clean_data.py:

✔️ داده خام را تمیز می‌کند
✔️ خطاهای رایج را حذف می‌کند
✔️ ستون مالی می‌سازد
✔️ فروش روزانه تولید می‌کند
✔️ پایه‌ی تمام مدل‌هاست