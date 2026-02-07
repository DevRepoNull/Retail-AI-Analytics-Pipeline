import os
from kaggle.api.kaggle_api_extended import KaggleApi

def download_dataset():
    api = KaggleApi()
    api.authenticate()

    dataset = "tunguz/online-retail"  # نمونه
    path = "data/raw"
    os.makedirs(path, exist_ok=True)

    api.dataset_download_files(dataset, path=path, unzip=True)
    print("Dataset downloaded!")

if __name__ == "__main__":
    download_dataset()