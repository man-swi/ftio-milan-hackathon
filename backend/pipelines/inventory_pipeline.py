import pandas as pd


class InventoryPipeline:

    def __init__(self, file_path):

        self.file_path = file_path
        self.df = None

    def load_data(self):

        self.df = pd.read_csv(self.file_path)

        print("INVENTORY DATA LOADED")
        print(self.df.head())

        return self.df

    def standardize_columns(self):

        self.df.columns = [
            col.strip().lower().replace(" ", "_")
            for col in self.df.columns
        ]

        return self.df

    def validate_required_columns(self):

        required_columns = [
            "sku",
            "product_name",
            "category",
            "stock",
            "unit_price",
            "sales_velocity"
        ]

        missing_columns = []

        for col in required_columns:

            if col not in self.df.columns:
                missing_columns.append(col)

        if missing_columns:

            raise ValueError(
                f"Missing required columns: {missing_columns}"
            )

        print("INVENTORY SCHEMA VALIDATED")

    def clean_missing_values(self):

        self.df = self.df.dropna(
            subset=[
                "sku",
                "product_name",
                "stock",
                "unit_price"
            ]
        )

        self.df["stock"] = (
            self.df["stock"]
            .fillna(0)
            .astype(int)
        )

        self.df["unit_price"] = (
            self.df["unit_price"]
            .fillna(0)
            .astype(float)
        )

        return self.df

    def create_inventory_features(self):

        self.df["inventory_value"] = (
            self.df["stock"] *
            self.df["unit_price"]
        )

        self.df["stock_status"] = self.df["stock"].apply(
            lambda x:
            "LOW" if x < 20
            else "MEDIUM" if x < 100
            else "HIGH"
        )

        return self.df

    def run_pipeline(self):

        self.load_data()

        self.standardize_columns()

        self.validate_required_columns()

        self.clean_missing_values()

        self.create_inventory_features()

        print("INVENTORY PIPELINE COMPLETED")

        return self.df


if __name__ == "__main__":

    pipeline = InventoryPipeline(
        "backend/data/current_inventory.csv"
    )

    df = pipeline.run_pipeline()

    print(df.head())