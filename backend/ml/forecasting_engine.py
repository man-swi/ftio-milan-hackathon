import os
import joblib
import pandas as pd

from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error

from backend.services.data_engine import (
    data_engine
)


MODEL_PATH = (
    "backend/models/"
    "demand_forecasting_model.pkl"
)


class DemandForecastingEngine:

    def __init__(self):

        self.model = None

        self.df = None

        self.feature_columns = None

        self.target_column = "future_demand"

    # -----------------------------------
    # LOAD TRAINING DATA
    # -----------------------------------

    def load_training_data(self):

        inventory_df = (
            data_engine.load_inventory_data()
        )

        df = inventory_df.copy()

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

        print(
            "FORECAST TRAINING DATA LOADED"
        )

        return self.df

    # -----------------------------------
    # FEATURE ENGINEERING
    # -----------------------------------

    def create_training_features(self):

        df = self.df.copy()

        velocity_multiplier = {

            "low": 0.3,

            "medium": 0.6,

            "high": 1.0
        }

        df["units_sold"] = (

            df["stock"]
            *
            df["sales_velocity"]
            .str.lower()
            .map(velocity_multiplier)
            .fillna(0.5)

        )

        df["future_demand"] = (

            (
                df["trend_score"]
                *
                df["units_sold"]
            ) / 100

        )

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

        self.feature_columns = [

            "trend_score",

            "units_sold",

            "unit_price",

            "stock",

            "sales_velocity_encoded"
        ]

        self.df = df

        print(
            "FORECAST FEATURES ENGINEERED"
        )

        return self.df

    # -----------------------------------
    # TRAIN MODEL
    # -----------------------------------

    def train_model(self):

        X = self.df[
            self.feature_columns
        ]

        y = self.df[
            self.target_column
        ]

        X_train, X_test, y_train, y_test = (
            train_test_split(

                X,
                y,

                test_size=0.2,

                random_state=42
            )
        )

        self.model = (
            RandomForestRegressor(

                n_estimators=100,

                random_state=42
            )
        )

        self.model.fit(
            X_train,
            y_train
        )

        predictions = (
            self.model.predict(X_test)
        )

        mae = mean_absolute_error(

            y_test,
            predictions
        )

        print("MODEL TRAINED")

        print(
            f"Mean Absolute Error: "
            f"{mae:.2f}"
        )

        return mae

    # -----------------------------------
    # SAVE MODEL
    # -----------------------------------

    def save_model(self):

        joblib.dump(
            self.model,
            MODEL_PATH
        )

        print(
            "FORECAST MODEL SAVED"
        )

    # -----------------------------------
    # LOAD MODEL
    # -----------------------------------

    def load_model(self):

        if os.path.exists(MODEL_PATH):

            self.model = joblib.load(
                MODEL_PATH
            )

            print(
                "FORECAST MODEL LOADED"
            )

            return True

        return False

    # -----------------------------------
    # PREDICT FUTURE DEMAND
    # -----------------------------------

    def predict_future_demand(

        self,
        input_data

    ):

        input_df = pd.DataFrame([
            input_data
        ])

        input_df = input_df[
            self.feature_columns
        ]

        prediction = (
            self.model.predict(
                input_df
            )[0]
        )

        return round(
            prediction,
            2
        )

    # -----------------------------------
    # MAIN PIPELINE
    # -----------------------------------

    def run_pipeline(self):

        # TRY LOADING MODEL FIRST

        model_loaded = (
            self.load_model()
        )

        if model_loaded:

            print(
                "USING EXISTING MODEL"
            )

            # Still needed for feature order
            self.create_feature_schema()

            return

        print(
            "NO EXISTING MODEL FOUND"
        )

        print(
            "TRAINING NEW MODEL..."
        )

        self.load_training_data()

        self.create_training_features()

        self.train_model()

        self.save_model()

        print(
            "FTIO FORECASTING ENGINE READY"
        )

    # -----------------------------------
    # FEATURE SCHEMA RESTORE
    # -----------------------------------

    def create_feature_schema(self):

        self.feature_columns = [

            "trend_score",

            "units_sold",

            "unit_price",

            "stock",

            "sales_velocity_encoded"
        ]


forecasting_engine = (
    DemandForecastingEngine()
)


if __name__ == "__main__":

    forecasting_engine.run_pipeline()

    sample_prediction = (

        forecasting_engine
        .predict_future_demand(

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