# forecasting.py
import streamlit as st
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error

st.set_page_config(page_title="Retail Sales Forecasting", layout="wide")
st.title("📈 Retail Sales Forecasting Dashboard")

# --- Load Data ---
@st.cache_data
def load_data(path="data/clean/daily_sales.csv"):
    df = pd.read_csv(path)
    df["Date"] = pd.to_datetime(df["Date"])
    df = df.sort_values("Date").reset_index(drop=True)
    return df

df = load_data()
st.subheader("Historical Daily Sales (Top 10)")
st.dataframe(df.head(10))

# --- Feature Engineering ---
df["lag_1"] = df["TotalPrice"].shift(1)
df["lag_7"] = df["TotalPrice"].shift(7)
df["rolling_mean_7"] = df["TotalPrice"].rolling(7).mean()
df = df.dropna().reset_index(drop=True)

# --- Train/Test Split ---
split_date = df["Date"].quantile(0.8)
train = df[df["Date"] <= split_date]
test = df[df["Date"] > split_date]

X_train = train[["lag_1", "lag_7", "rolling_mean_7"]]
y_train = train["TotalPrice"]
X_test = test[["lag_1", "lag_7", "rolling_mean_7"]]
y_test = test["TotalPrice"]

# --- Model Selection ---
st.subheader("Select Forecasting Model")
model_option = st.selectbox("Model", ["Linear Regression", "Random Forest"])

if model_option == "Linear Regression":
    model = LinearRegression()
else:
    model = RandomForestRegressor(n_estimators=200, random_state=42)

# --- Train Model ---
model.fit(X_train, y_train)
predictions = model.predict(X_test)

# --- Evaluation ---
mae = mean_absolute_error(y_test, predictions)
rmse = np.sqrt(mean_squared_error(y_test, predictions))

st.write(f"**Model:** {model_option}")
st.write(f"**MAE:** {mae:.2f}")
st.write(f"**RMSE:** {rmse:.2f}")

# --- Forecast DataFrame ---
forecast = test.copy()
forecast["Prediction"] = predictions

# --- Date Range Selector ---
st.subheader("Select Date Range for Visualization")

# تبدیل Timestamp پانداز به datetime استاندارد پایتون
min_date = forecast["Date"].min().to_pydatetime()
max_date = forecast["Date"].max().to_pydatetime()

date_range = st.slider(
    "Date Range",
    min_value=min_date,
    max_value=max_date,
    value=(min_date, max_date), # مقدار اولیه اسلایدر
    format="YYYY-MM-DD"
)

# فیلتر کردن داده‌ها بر اساس انتخاب کاربر
# نکته: چون از slider خروجی گرفتیم، تاریخ‌ها را به Timestamp برمی‌گردانیم تا با ستون Date همخوانی داشته باشند
filtered_forecast = forecast[
    (forecast["Date"] >= pd.Timestamp(date_range[0])) & 
    (forecast["Date"] <= pd.Timestamp(date_range[1]))
]

# --- Interactive Line Chart ---
st.subheader("Forecast vs Real Sales")
st.line_chart(filtered_forecast.set_index("Date")[["TotalPrice", "Prediction"]])

# --- Save CSV ---
output_path = "output/sales_forecast.csv"
forecast.to_csv(output_path, index=False)
st.success(f"Forecast saved to `{output_path}`")
