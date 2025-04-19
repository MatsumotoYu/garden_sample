# src/components/stores.py
import pandas as pd

def get_stores(location: str):
    # stores.csv からデータを読み込み
    df = pd.read_csv("data/stores.csv")
    # 簡易的なフィルタリング（実際は Google Maps API を使う想定）
    stores = df[df["city"].str.contains(location, na=False)].to_dict("records")
    return stores