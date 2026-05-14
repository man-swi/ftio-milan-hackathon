import pandas as pd


class SalesPipeline:

    def __init__(self, file_path):

        self.file_path = file_path
        self.df = None

    def load_data(self):

        self.df = pd.read_csv(self.file_path)

        print("SALES DATA LOADED")
        print(self.df.head())

        return self.df

    def standardize_columns(self):

        self.df.columns = [
            col.strip().lower().replace(" ", "_")
            for col in self.df.columns
        ]

        return self.df

    def clean_missing_values(self):

        self.df = self.df.dropna()

        return self.df

    def convert_dates(self):

        if "date_purchase" in self.df.columns:

            self.df["date_purchase"] = pd.to_datetime(
                self.df["date_purchase"],
                errors="coerce"
            )

        return self.df

    def create_sales_features(self):

        if "purchase_amount_(usd)" in self.df.columns:

            self.df["purchase_amount_(usd)"] = (
                self.df["purchase_amount_(usd)"]
                .astype(float)
            )

        # Revenue segmentation

        self.df["revenue_segment"] = (
            self.df["purchase_amount_(usd)"]
            .apply(
                lambda x:
                "LOW" if x < 50
                else "MEDIUM" if x < 150
                else "HIGH"
            )
        )

        # Customer rating signal

        if "review_rating" in self.df.columns:

            self.df["review_signal"] = (
                self.df["review_rating"]
                .apply(
                    lambda x:
                    "POSITIVE" if x >= 4
                    else "NEGATIVE"
                )
            )

        return self.df

    def generate_temporal_metrics(self):

        if "date_purchase" not in self.df.columns:

            return self.df

        # Daily revenue

        daily_sales = (
            self.df
            .groupby("date_purchase")[
                "purchase_amount_(usd)"
            ]
            .sum()
            .reset_index()
        )

        daily_sales.columns = [
            "date",
            "daily_revenue"
        ]

        self.daily_sales = daily_sales

        print("TEMPORAL SALES METRICS GENERATED")

        return self.df

    def run_pipeline(self):

        self.load_data()

        self.standardize_columns()

        self.clean_missing_values()

        self.convert_dates()

        self.create_sales_features()

        self.generate_temporal_metrics()

        print("SALES PIPELINE COMPLETED")

        return self.df


if __name__ == "__main__":

    pipeline = SalesPipeline(
        "backend/data/Fashion_Retail_Sales.csv"
    )

    df = pipeline.run_pipeline()

    print(df.head())

    print("\nDAILY SALES SAMPLE\n")

    print(pipeline.daily_sales.head())