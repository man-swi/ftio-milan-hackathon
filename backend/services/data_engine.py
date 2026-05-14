from backend.pipelines.inventory_pipeline import (
    InventoryPipeline
)

from backend.pipelines.sales_pipeline import (
    SalesPipeline
)

from backend.pipelines.trend_pipeline import (
    TrendPipeline
)


class FTIODataEngine:

    def __init__(self):

        self.inventory_df = None

        self.sales_df = None

        self.trend_df = None

    def load_inventory_data(self):

        pipeline = InventoryPipeline(
            "backend/data/current_inventory.csv"
        )

        self.inventory_df = (
            pipeline.run_pipeline()
        )

        return self.inventory_df

    def load_sales_data(self):

        pipeline = SalesPipeline(
            "backend/data/Fashion_Retail_Sales.csv"
        )

        self.sales_df = (
            pipeline.run_pipeline()
        )

        return self.sales_df

    def load_trend_data(self):

        pipeline = TrendPipeline(
            "backend/data/shopify_trending_products_2025.csv"
        )

        self.trend_df = (
            pipeline.run_pipeline()
        )

        return self.trend_df

    def load_all_data(self):

        print("\nLOADING FTIO ENTERPRISE DATA ENGINE\n")

        self.load_inventory_data()

        self.load_sales_data()

        self.load_trend_data()

        print("\nFTIO DATA ENGINE READY\n")

        return {
            "inventory": self.inventory_df,
            "sales": self.sales_df,
            "trends": self.trend_df
        }


data_engine = FTIODataEngine()


if __name__ == "__main__":

    data = data_engine.load_all_data()

    print("\nINVENTORY DATA\n")
    print(data["inventory"].head())

    print("\nSALES DATA\n")
    print(data["sales"].head())

    print("\nTREND DATA\n")
    print(data["trends"].head())