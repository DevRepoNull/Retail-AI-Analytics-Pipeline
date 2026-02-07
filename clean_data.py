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