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

    # -----------------------------------
    # NO PREVIOUS HISTORY
    # -----------------------------------

    if previous_data is None:

        return {

            "previous_momentum": None,

            "current_momentum":
            current_momentum,

            "momentum_change": 0,

            "acceleration_label":
            "NEW TREND",

            "trend_status":
            "NEW TREND"
        }

    # -----------------------------------
    # HISTORICAL VALUES
    # -----------------------------------

    previous_momentum = (
        previous_data["momentum"]
    )

    previous_confidence = (
        previous_data.get(
            "confidence",
            None
        )
    )

    # -----------------------------------
    # MOMENTUM DELTA
    # -----------------------------------

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

    # -----------------------------------
    # TREND LABELS
    # -----------------------------------

    acceleration_label = "STABLE"

    trend_status = "STABLE"

    if momentum_change >= 25:

        acceleration_label = (
            "HIGH ACCELERATION"
        )

        trend_status = (
            "ACCELERATING"
        )

    elif momentum_change >= 10:

        acceleration_label = (
            "RISING"
        )

        trend_status = (
            "RISING"
        )

    elif momentum_change <= -20:

        acceleration_label = (
            "SHARP DECLINE"
        )

        trend_status = (
            "DECLINING"
        )

    elif momentum_change <= -10:

        acceleration_label = (
            "DECLINING"
        )

        trend_status = (
            "DECLINING"
        )

    # -----------------------------------
    # VOLATILITY SCORE
    # -----------------------------------

    volatility_score = round(
        abs(momentum_change) * 1.5,
        2
    )

    # -----------------------------------
    # CONFIDENCE SHIFT
    # -----------------------------------

    confidence_shift = (
        calculate_confidence_shift(
            current_confidence=current_momentum,
            previous_confidence=previous_confidence
        )
    )

    # -----------------------------------
    # FINAL OUTPUT
    # -----------------------------------

    return {

        "previous_momentum":
        previous_momentum,

        "current_momentum":
        current_momentum,

        "momentum_change":
        momentum_change,

        "acceleration_label":
        acceleration_label,

        "trend_status":
        trend_status,

        "volatility_score":
        volatility_score,

        "confidence_shift":
        confidence_shift
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
# STOCKOUT RISK GROWTH
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