import pandas as pd

print("START")

df = pd.read_csv(
    "backend/data/inventory_sample.csv",
    encoding="utf-8",
    engine="python"
)

print("SUCCESS")

print(df.head())