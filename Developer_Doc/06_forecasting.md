# 📈 forecasting.py — پیش‌بینی سری زمانی فروش با داشبورد Streamlit

این ماژول همزمان دو کار انجام می‌دهد:

1️⃣ مدل‌سازی پیش‌بینی فروش روزانه (Linear Regression / Random Forest)  
2️⃣ ارائه‌ی نتایج به صورت **داشبورد تعاملی با Streamlit**

---

# 🎯 هدف این ماژول

- پیش‌بینی فروش آینده برای تصمیمات کسب‌وکار  
- مقایسه مدل‌ها به صورت تعاملی  
- امکان انتخاب بازه زمانی و مشاهده نمودار Real vs Prediction  
- خروجی CSV برای استفاده‌های بعدی  

---

# 🧭 جایگاه در Pipeline

data/clean/daily_sales.csv
↓
forecasting.py (Streamlit)
↓
output/sales_forecast.csv
↓
Dashboard Interactive

---

# 📥 ورودی داده

- data/clean/daily_sales.csv

---

# 📤 خروجی‌ها

- output/sales_forecast.csv → شامل تاریخ، مقدار واقعی، و مقدار پیش‌بینی شده  
- نمایش interactive chart در Streamlit  

---

# 🧩 کتابخانه‌های استفاده‌شده

- pandas / numpy → داده و محاسبات عددی  
- sklearn → مدل‌ها و متریک‌ها  
- streamlit → داشبورد تعاملی  
- matplotlib (اختیاری) → نمودارها  

---

# 🔍 توضیح خط‌به‌خط کد

---

## 🏷️ Streamlit Setup

```python
st.set_page_config(page_title="Retail Sales Forecasting", layout="wide")
st.title("📈 Retail Sales Forecasting Dashboard")
```


---

# 📥 ورودی داده

- data/clean/daily_sales.csv

---

# 📤 خروجی‌ها

- output/sales_forecast.csv → شامل تاریخ، مقدار واقعی، و مقدار پیش‌بینی شده  
- نمایش interactive chart در Streamlit  

---

# 🧩 کتابخانه‌های استفاده‌شده

- pandas / numpy → داده و محاسبات عددی  
- sklearn → مدل‌ها و متریک‌ها  
- streamlit → داشبورد تعاملی  
- matplotlib (اختیاری) → نمودارها  

---

# 🔍 توضیح خط‌به‌خط کد

---

## 🏷️ Streamlit Setup

```python
st.set_page_config(page_title="Retail Sales Forecasting", layout="wide")
st.title("📈 Retail Sales Forecasting Dashboard")
```

تنظیم عنوان و Layout داشبورد.

---

## 📂 بارگذاری داده‌ها

```
@st.cache_data
def load_data(path="data/clean/daily_sales.csv"):
    df = pd.read_csv(path)
    df["Date"] = pd.to_datetime(df["Date"])
    df = df.sort_values("Date").reset_index(drop=True)
    return df

df = load_data()
```


- @st.cache_data → داده یکبار بارگذاری می‌شود و سرعت داشبورد افزایش می‌یابد

- تاریخ به datetime تبدیل می‌شود

- مرتب‌سازی زمانی برای پیش‌بینی ضروری است

---

## 🧮 Feature Engineering

```
df["lag_1"] = df["TotalPrice"].shift(1)
df["lag_7"] = df["TotalPrice"].shift(7)
df["rolling_mean_7"] = df["TotalPrice"].rolling(7).mean()
df = df.dropna().reset_index(drop=True)
```

- lag_1 → مقدار دیروز

- lag_7 → مقدار یک هفته قبل

- rolling_mean_7 → میانگین متحرک هفت روزه

این ویژگی‌ها باعث می‌شوند مدل روندهای زمانی کوتاه‌مدت را تشخیص دهد.

---

## ✂️ Train/Test Split

```
split_date = df["Date"].quantile(0.8)
train = df[df["Date"] <= split_date]
test = df[df["Date"] > split_date]
```

- ۸۰٪ داده برای آموزش

- ۲۰٪ داده آخر برای تست

---

## 🎯 انتخاب مدل

```
model_option = st.selectbox("Model", ["Linear Regression", "Random Forest"])
```

- کاربر می‌تواند مدل را انتخاب کند

- Linear Regression → ساده و قابل تفسیر

- Random Forest → غیرخطی و مقاوم در برابر نویز

---

## 🔄 آموزش مدل

```
model.fit(X_train, y_train)
predictions = model.predict(X_test)
```

- مدل آموزش داده می‌شود

- پیش‌بینی روی تست انجام می‌شود

---

## 📏 ارزیابی مدل

```
mae = mean_absolute_error(y_test, predictions)
rmse = np.sqrt(mean_squared_error(y_test, predictions))
st.write(f"**MAE:** {mae:.2f}")
st.write(f"**RMSE:** {rmse:.2f}")
```

- نمایش metirc تعاملی برای انتخاب بهترین مدل

---

## 📊 آماده‌سازی داده برای نمایش

```
forecast = test.copy()
forecast["Prediction"] = predictions
```

---

## 📅 انتخاب بازه زمانی برای نمودار

```
date_range = st.slider("Date Range", min_value=min_date, max_value=max_date, value=(min_date, max_date), format="YYYY-MM-DD")
filtered_forecast = forecast[(forecast["Date"] >= pd.Timestamp(date_range[0])) & (forecast["Date"] <= pd.Timestamp(date_range[1]))]
```

- کاربران می‌توانند بازه زمانی دلخواه را برای نمایش انتخاب کنند

---

## 📈 نمودار تعاملی

```
st.line_chart(filtered_forecast.set_index("Date")[["TotalPrice", "Prediction"]])
```

- نمایش فروش واقعی و پیش‌بینی شده در یک نمودار تعاملی

---

## 💾 ذخیره CSV

```
output_path = "output/sales_forecast.csv"
forecast.to_csv(output_path, index=False)
st.success(f"Forecast saved to `{output_path}`")
```
- ذخیره داده برای تحلیل‌های بعدی یا داشبوردهای دیگر
---

# 🧠 نکات فنی

- streamlit → نمایش سریع و تعاملی

- ویژگی‌های سری زمانی ساده → baseline مناسب

- امکان اضافه کردن مدل‌های پیچیده‌تر مثل Prophet یا LSTM

---

# ✅ جمع‌بندی

forecasting.py:

✔️ مدل‌های پیش‌بینی فروش را اجرا می‌کند
✔️ امکان انتخاب مدل و بازه زمانی دارد
✔️ خروجی CSV و نمودار تعاملی می‌دهد
✔️ پایه داشبورد عملیاتی Retail AI است