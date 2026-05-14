import pandas as pd


class TrendPipeline:

    def __init__(self, file_path):

        self.file_path = file_path
        self.df = None

    def load_data(self):

        self.df = pd.read_csv(self.file_path)

        print("TREND DATA LOADED")
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

    def create_trend_features(self):

        # Normalize trend score

        if "trend_score" in self.df.columns:

            max_score = self.df["trend_score"].max()

            self.df["normalized_trend_score"] = (
                self.df["trend_score"] / max_score
            )

        # Revenue opportunity

        if (
            "units_sold" in self.df.columns and
            "price" in self.df.columns
        ):

            self.df["revenue_opportunity"] = (
                self.df["units_sold"] *
                self.df["price"]
            )

        # Trend classification

        if "trend_score" in self.df.columns:

            self.df["trend_strength"] = (
                self.df["trend_score"]
                .apply(
                    lambda x:
                    "EXPLOSIVE" if x >= 80
                    else "ACCELERATING" if x >= 60
                    else "STABLE"
                )
            )

        return self.df

    def generate_market_insights(self):

        top_trends = (
            self.df
            .sort_values(
                by="trend_score",
                ascending=False
            )
            .head(5)
        )

        self.top_trends = top_trends

        print("MARKET INSIGHTS GENERATED")

    def run_pipeline(self):

        self.load_data()

        self.standardize_columns()

        self.clean_missing_values()

        self.create_trend_features()

        self.generate_market_insights()

        print("TREND PIPELINE COMPLETED")

        return self.df


if __name__ == "__main__":

    pipeline = TrendPipeline(
        "backend/data/shopify_trending_products_2025.csv"
    )

    df = pipeline.run_pipeline()

    print(df.head())

    print("\nTOP MARKET TRENDS\n")

    print(pipeline.top_trends.head())