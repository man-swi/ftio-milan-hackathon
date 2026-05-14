import pandas as pd

from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error

from backend.services.data_engine import (
    data_engine
)


class DemandForecastingEngine:

    def __init__(self):

        self.model = RandomForestRegressor(
            n_estimators=100,
            random_state=42
        )

        self.df = None

        self.feature_columns = None

        self.target_column = "future_demand"

    def load_training_data(self):

        inventory_df = data_engine.load_inventory_data()

        # Use inventory dataset as foundation
        df = inventory_df.copy()

        # Synthetic trend scores by category
        trend_scores = {
            "tops": 75,
            "outerwear": 82,
            "blazers": 88,
            "pants": 65,
            "knitwear": 70,
            "bottoms": 68
        }

        df["trend_score"] = (
            df["category"]
            .map(trend_scores)
            .fillna(70)
        )

        self.df = df

        print("FORECAST TRAINING DATA LOADED")

        return self.df

    def create_training_features(self):

        df = self.df.copy()

        # Sales velocity multipliers
        velocity_multiplier = {
            "low": 0.3,
            "medium": 0.6,
            "high": 1.0
        }

        # Create synthetic units sold
        df["units_sold"] = (
            df["stock"] *
            df["sales_velocity"]
            .str.lower()
            .map(velocity_multiplier)
            .fillna(0.5)
        )

        # Create future demand target
        df["future_demand"] = (
            (
                df["trend_score"] *
                df["units_sold"]
            ) / 100
        )

        # Encode sales velocity
        velocity_map = {
            "low": 1,
            "medium": 2,
            "high": 3
        }

        df["sales_velocity_encoded"] = (
            df["sales_velocity"]
            .str.lower()
            .map(velocity_map)
        )

        # FINAL FEATURE ORDER
        self.feature_columns = [
            "trend_score",
            "units_sold",
            "unit_price",
            "stock",
            "sales_velocity_encoded"
        ]

        self.df = df

        print("FORECAST FEATURES ENGINEERED")

        return self.df

    def train_model(self):

        X = self.df[self.feature_columns]

        y = self.df[self.target_column]

        X_train, X_test, y_train, y_test = train_test_split(
            X,
            y,
            test_size=0.2,
            random_state=42
        )

        self.model.fit(X_train, y_train)

        predictions = self.model.predict(X_test)

        mae = mean_absolute_error(
            y_test,
            predictions
        )

        print("MODEL TRAINED")
        print(f"Mean Absolute Error: {mae:.2f}")

        return mae

    def predict_future_demand(
        self,
        input_data
    ):

        input_df = pd.DataFrame([input_data])

        # FORCE SAME FEATURE ORDER
        input_df = input_df[
            self.feature_columns
        ]

        prediction = self.model.predict(
            input_df
        )[0]

        return round(prediction, 2)

    def run_pipeline(self):

        self.load_training_data()

        self.create_training_features()

        self.train_model()

        print("FTIO FORECASTING ENGINE READY")


forecasting_engine = (
    DemandForecastingEngine()
)


if __name__ == "__main__":

    forecasting_engine.run_pipeline()

    sample_prediction = (
        forecasting_engine.predict_future_demand(
            {
                "trend_score": 92,
                "units_sold": 1400,
                "unit_price": 45,
                "stock": 18,
                "sales_velocity_encoded": 3
            }
        )
    )

    print(
        f"\nPredicted Future Demand: "
        f"{sample_prediction}"
    )