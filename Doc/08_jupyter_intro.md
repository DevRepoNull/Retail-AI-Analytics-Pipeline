# 📓 Jupyter Notebook — مقدمه و کاربرد

## 🎯 هدف

Jupyter Notebook محیطی تعاملی برای **برنامه‌نویسی، تحلیل داده و مستندسازی علمی** است.  
با آن می‌توانید:

- کدهای Python را خط به خط اجرا کنید 🐍  
- نتایج محاسبات را فوری ببینید 📊  
- نمودارها و تصاویر را داخل نوت‌بوک نمایش دهید 🖼️  
- متن، توضیح و فرمول‌های LaTeX را ترکیب کنید 📝  

---

## 🧩 ویژگی‌ها

- محیط تعاملی برای تست الگوریتم‌ها  
- مناسب یادگیری و ارائه پروژه‌های علمی  
- پشتیبانی از پلاگین‌ها و visualization  
- قابلیت export به HTML یا PDF برای ارائه دانشگاهی  

---

## 💻 نصب و اجرا

### نصب با pip
```bash
pip install jupyter
```

### اجرای نوت‌بوک
```
jupyter notebook
```

- مرورگر باز می‌شود و مسیر فایل‌ها را نمایش می‌دهد

- می‌توانید سلول‌های کد و متن اضافه کنید


### گزینه دیگر: JupyterLab
```
pip install jupyterlab
jupyter lab
```

- محیط مدرن‌تر و حرفه‌ای‌تر با پشتیبانی از چند تب و ابزارهای پیشرفته

---

# 🧠 نکات کاربردی

- هر سلول می‌تواند کد Python یا Markdown باشد

- Shift + Enter → اجرای سلول

- Ctrl + Enter → اجرای سلول بدون رفتن به سلول بعدی

- %%timeit → اندازه‌گیری زمان اجرا

- !command → اجرای دستور shell داخل سلول

---

# 🚀 کاربرد در پروژه Retail AI

- تحلیل داده‌های فروش

- نمایش نمودار و جدول تعاملی

- تست ماژول‌های مختلف قبل از انتقال به Streamlit

- تولید گزارش آموزشی و دانشگاهی


---

### 2️⃣ jupyter_code_reference.md

# 📝 Jupyter Notebook Code Reference — Retail AI

این فایل تمام **کدهای موجود در نوت‌بوک** را توضیح می‌دهد و کارکرد هر سلول را تشریح می‌کند.

---

## 1️⃣ Import Libraries

```python
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
```

- pandas → مدیریت داده‌ها

- numpy → محاسبات عددی

- matplotlib / seaborn → نمودار و visualization

---

## 2️⃣ Load Data

```
df = pd.read_csv("data/clean/retail_clean.csv")
df['InvoiceDate'] = pd.to_datetime(df['InvoiceDate'])
```

- خواندن داده تمیز شده

- تبدیل ستون تاریخ به datetime

---

## 3️⃣ Exploratory Data Analysis (EDA)

```
plt.hist(df['TotalPrice'], bins=50)
plt.show()
```

- توزیع فروش را نمایش می‌دهد

- شناسایی outlier و توزیع داده

---

## 4️⃣ Feature Engineering

```
df['lag_1'] = df['TotalPrice'].shift(1)
df['rolling_mean_7'] = df['TotalPrice'].rolling(7).mean()
```

- lag → مقدار دیروز

- rolling_mean → میانگین متحرک

## 5️⃣ Model Training

```
from sklearn.linear_model import LinearRegression
model = LinearRegression()
model.fit(X_train, y_train)
```

- آموزش مدل پیش‌بینی

- تست Linear Regression یا Random Forest

---

## 6️⃣ Evaluation

```
from sklearn.metrics import mean_absolute_error
mae = mean_absolute_error(y_test, predictions)
```

- ارزیابی مدل با MAE و RMSE

---

## 7️⃣ Visualization

```
plt.plot(df['Date'], df['TotalPrice'])
plt.scatter(df_anomaly['Date'], df_anomaly['TotalPrice'])
plt.show()
```

- نمایش نمودارهای فروش و ناهنجاری‌ها

---

## 8️⃣ RFM Analysis

```
rfm = df.groupby('CustomerID').agg({
    'InvoiceDate': lambda x: (snapshot_date - x.max()).days,
    'InvoiceNo': 'count',
    'TotalPrice': 'sum'
})
```

- محاسبه Recency, Frequency, Monetary برای مشتریان

---

## 9️⃣ Clustering

```
from sklearn.cluster import KMeans
kmeans = KMeans(n_clusters=4, random_state=42)
rfm['Cluster'] = kmeans.fit_predict(rfm_scaled)
```

- خوشه‌بندی مشتریان بر اساس RFM

---

## 🔟 Anomaly Detection

```
from sklearn.ensemble import IsolationForest
model = IsolationForest(contamination=0.02)
df['anomaly'] = model.fit_predict(features)
```

- شناسایی نقاط غیرعادی در فروش روزانه