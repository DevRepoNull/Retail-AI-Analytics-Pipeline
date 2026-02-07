# 📈 03_forecasting.ipynb — پیش‌بینی فروش روزانه

این نوت‌بوک برای **مدل‌سازی و پیش‌بینی فروش روزانه** با استفاده از Linear Regression و Random Forest استفاده می‌شود.

---

## 📌 بخش 1 — بارگذاری کتابخانه و داده‌ها

```python
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error

daily = pd.read_csv("../data/clean/daily_sales.csv")
daily["Date"] = pd.to_datetime(daily["Date"])
daily = daily.sort_values("Date")
```

- pandas / numpy → مدیریت و محاسبات داده

- matplotlib → رسم نمودارها

- sklearn → مدل‌های پیش‌بینی و ارزیابی

- داده روزانه بارگذاری و مرتب‌سازی شده بر اساس تاریخ

---

## 📌 بخش 2 — Feature Engineering

```
df = daily.copy()

df["lag_1"] = df["TotalPrice"].shift(1)
df["lag_7"] = df["TotalPrice"].shift(7)

df["rolling_mean_7"] = df["TotalPrice"].rolling(7).mean()

df = df.dropna()
```

- ایجاد ویژگی‌های زمانی:

 - lag_1 → فروش دیروز

 - lag_7 → فروش ۷ روز قبل

 - rolling_mean_7 → میانگین متحرک ۷ روزه

- حذف رکوردهای با مقادیر NA

---

## 📌 بخش 3 — تقسیم داده به Train/Test

```
split_date = df["Date"].quantile(0.8)

train = df[df["Date"] <= split_date]
test = df[df["Date"] > split_date]

X_train = train[["lag_1", "lag_7", "rolling_mean_7"]]
y_train = train["TotalPrice"]

X_test = test[["lag_1", "lag_7", "rolling_mean_7"]]
y_test = test["TotalPrice"]
```

- ۸۰٪ داده‌ها → Train

- ۲۰٪ داده‌ها → Test

- X → ویژگی‌ها، y → هدف (TotalPrice)

---

## 📌 بخش 4 — Linear Regression

```
lr = LinearRegression()
lr.fit(X_train, y_train)

pred_lr = lr.predict(X_test)

rmse = np.sqrt(mean_squared_error(y_test, pred_lr))
print("Linear RMSE:", rmse)
```

- مدل Linear Regression آموزش داده می‌شود

- پیش‌بینی روی داده Test

- محاسبه RMSE برای سنجش دقت مدل

---

## 📌 بخش 5 — تکرار RMSE (اختیاری)

```
from sklearn.metrics import mean_squared_error
import numpy as np

rmse = np.sqrt(mean_squared_error(y_test, pred_lr))
print("Linear RMSE:", rmse)
```

- تکرار محاسبه RMSE برای اطمینان از صحت عدد

---

## 📌 بخش 6 — Random Forest

```
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error

rf = RandomForestRegressor(n_estimators=200, random_state=42)
rf.fit(X_train, y_train)

pred_rf = rf.predict(X_test)

print("RF MAE:", mean_absolute_error(y_test, pred_rf))
rmse_rf = np.sqrt(mean_squared_error(y_test, pred_rf))
print("RF RMSE:", rmse_rf)
```

- آموزش مدل Random Forest

- پیش‌بینی روی داده Test

- ارزیابی با MAE و RMSE

---

## 📌 بخش 7 — رسم نمودار پیش‌بینی

```
plt.figure(figsize=(12,5))
plt.plot(test["Date"], y_test.values, label="Real")
plt.plot(test["Date"], pred_rf, label="Predicted")

plt.title("Daily Sales Forecast - Random Forest")
plt.xlabel("Date")
plt.ylabel("Sales")
plt.legend()
plt.show()
```

- نمایش فروش واقعی و پیش‌بینی شده با Random Forest

- بررسی بصری دقت مدل و نوسانات

---

# ✅ جمع‌بندی

forecasting:

- داده روزانه فروش را آماده‌سازی می‌کند

- ویژگی‌های زمانی برای پیش‌بینی ایجاد می‌کند

- مدل‌های Linear Regression و Random Forest را آموزش می‌دهد

- عملکرد مدل‌ها را با MAE و RMSE ارزیابی می‌کند

- نمودار پیش‌بینی‌ها را برای تحلیل بصری نمایش می‌دهد