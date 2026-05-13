import json

from datetime import datetime

from backend.services.memory_engine import (
    retrieve_previous_trend_data
)

from backend.services.temporal_analysis import (
    calculate_momentum_acceleration
)


# ===================================
# LOAD CURRENT TRENDS
# ===================================

def load_current_trends():

    with open(

        "backend/data/mock_trends.json",

        "r"

    ) as file:

        return json.load(file)


# ===================================
# TREND SPIKE DETECTION
# ===================================

def detect_trend_spikes():

    trends = load_current_trends()

    alerts = []

    # ===================================
    # PROCESS TRENDS
    # ===================================

    for trend in trends:

        trend_name = trend.get(
            "trend",
            "Unknown Trend"
        )

        current_momentum = trend.get(
            "momentum",
            0
        )

        confidence = trend.get(
            "confidence",
            0
        )

        previous_data = (
            retrieve_previous_trend_data(
                trend_name
            )
        )

        if previous_data:

            previous_momentum = (
                previous_data.get(
                    "momentum",
                    current_momentum
                )
            )

        else:

            previous_momentum = (
                current_momentum
            )

        # ===================================
        # CALCULATE CHANGE
        # ===================================

        momentum_change = round(

            (
                current_momentum -
                previous_momentum
            ) * 100,

            2
        )

        # ===================================
        # ACCELERATION ALERT
        # ===================================

        if momentum_change >= 10:

            alerts.append({

                "timestamp":
                str(datetime.now()),

                "type":
                "TREND_SPIKE",

                "trend":
                trend_name,

                "severity":
                "HIGH",

                "message":

                f"{trend_name} momentum "

                f"increased "

                f"{momentum_change}% "

                f"in the latest "

                f"monitoring cycle.",

                "confidence":
                confidence
            })

        # ===================================
        # TREND WEAKENING
        # ===================================

        elif momentum_change <= -10:

            alerts.append({

                "timestamp":
                str(datetime.now()),

                "type":
                "TREND_DECLINE",

                "trend":
                trend_name,

                "severity":
                "MEDIUM",

                "message":

                f"{trend_name} momentum "

                f"dropped "

                f"{abs(momentum_change)}% "

                f"in the latest "

                f"monitoring cycle.",

                "confidence":
                confidence
            })

        # ===================================
        # LOW CONFIDENCE WARNING
        # ===================================

        if confidence <= 0.5:

            alerts.append({

                "timestamp":
                str(datetime.now()),

                "type":
                "LOW_CONFIDENCE",

                "trend":
                trend_name,

                "severity":
                "LOW",

                "message":

                f"{trend_name} confidence "

                f"fell below stability "

                f"threshold.",

                "confidence":
                confidence
            })

    return alerts