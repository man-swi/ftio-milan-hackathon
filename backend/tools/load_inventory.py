import pandas as pd

def load_inventory():
    return pd.read_csv("backend/data/inventory_sample.csv")

if __name__ == "__main__":
    print(load_inventory())