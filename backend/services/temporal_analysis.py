from backend.services.memory_engine import (
    retrieve_previous_trend_data
)


# -----------------------------------
# MOMENTUM ACCELERATION
# -----------------------------------

def calculate_momentum_acceleration(
    trend_name,
    current_momentum
):

    previous_data = (
        retrieve_previous_trend_data(
            trend_name
        )
    )

    if previous_data is None:

        return {

            "previous_momentum": None,

            "current_momentum":
            current_momentum,

            "momentum_change": 0,

            "acceleration_label":
            "NEW TREND"
        }

    previous_momentum = (
        previous_data["momentum"]
    )

    momentum_change = round(
        (
            (
                current_momentum -
                previous_momentum
            ) /
            max(previous_momentum, 0.01)
        ) * 100,
        2
    )

    acceleration_label = "STABLE"

    if momentum_change >= 25:

        acceleration_label = (
            "HIGH ACCELERATION"
        )

    elif momentum_change >= 10:

        acceleration_label = (
            "RISING"
        )

    elif momentum_change <= -15:

        acceleration_label = (
            "DECLINING"
        )

    return {

        "previous_momentum":
        previous_momentum,

        "current_momentum":
        current_momentum,

        "momentum_change":
        momentum_change,

        "acceleration_label":
        acceleration_label
    }


# -----------------------------------
# CONFIDENCE SHIFT
# -----------------------------------

def calculate_confidence_shift(
    current_confidence,
    previous_confidence
):

    if previous_confidence is None:

        return 0

    return round(
        (
            current_confidence -
            previous_confidence
        ) * 100,
        2
    )


# -----------------------------------
# RISK GROWTH
# -----------------------------------

def detect_risk_growth(
    current_risk,
    previous_risk
):

    risk_map = {

        "LOW": 1,
        "MEDIUM": 2,
        "HIGH": 3,
        "CRITICAL": 4
    }

    current_score = risk_map.get(
        current_risk,
        1
    )

    previous_score = risk_map.get(
        previous_risk,
        1
    )

    if current_score > previous_score:

        return "RISK INCREASING"

    elif current_score < previous_score:

        return "RISK REDUCING"

    return "RISK STABLE"