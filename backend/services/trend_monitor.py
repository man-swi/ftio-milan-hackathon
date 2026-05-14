from datetime import datetime

from backend.services.data_engine import (
    data_engine
)


def load_current_trends():

    if data_engine.trend_df is None:

        data_engine.load_trend_data()

    return data_engine.trend_df


def detect_trend_spikes():

    trend_df = load_current_trends()

    alerts = []

    # Sort by trend score and keep only top 10 signals
    top_trends = trend_df.sort_values(
        by="normalized_trend_score",
        ascending=False
    ).head(10)

    for _, row in top_trends.iterrows():

        trend_score = row.get(
            "trend_score",
            0
        )

        trend_strength = row.get(
            "trend_strength",
            "STABLE"
        )

        product_name = row.get(
            "product_name",
            "Unknown Product"
        )

        category = row.get(
            "category",
            "Unknown Category"
        )

        if (
            trend_strength == "EXPLOSIVE"
            and trend_score >= 95
        ):

            alert = {
                "timestamp": str(datetime.now()),
                "type": "TREND_SPIKE",
                "product": product_name,
                "category": category,
                "trend_score": trend_score,
                "severity": "HIGH",
                "message": (
                    f"{product_name} trend momentum "
                    f"reached explosive levels."
                )
            }

            alerts.append(alert)

        elif trend_strength == "ACCELERATING":

            alert = {
                "timestamp": str(datetime.now()),
                "type": "TREND_ACCELERATION",
                "product": product_name,
                "category": category,
                "trend_score": trend_score,
                "severity": "MEDIUM",
                "message": (
                    f"{product_name} trend is accelerating."
                )
            }

            alerts.append(alert)

    if alerts:

        print(f"Detected {len(alerts)} trend anomalies.")

    else:

        print("No trend anomalies detected.")

    return alerts