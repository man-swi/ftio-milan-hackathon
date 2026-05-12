import math


# -----------------------------------
# SALES VELOCITY MULTIPLIERS
# -----------------------------------

SALES_VELOCITY_MAP = {
    "low": 0.8,
    "medium": 1.0,
    "high": 1.4
}

# -----------------------------------
# SEASONAL CATEGORY MULTIPLIERS
# -----------------------------------

SEASONAL_MULTIPLIERS = {
    "tops": 1.2,
    "jackets": 1.1,
    "blazers": 1.0,
    "pants": 0.9
}


# -----------------------------------
# SELL OUT PROBABILITY
# -----------------------------------

def simulate_sellout_probability(
    momentum,
    confidence,
    current_stock,
    recommended_stock
):

    demand_pressure = (
        momentum *
        confidence *
        100
    )

    stock_ratio = current_stock / max(
        recommended_stock,
        1
    )

    probability = (
        demand_pressure / 100
    ) * (1 - min(stock_ratio, 1))

    probability = max(
        0.05,
        min(probability, 0.99)
    )

    return round(probability, 2)


# -----------------------------------
# RESTOCK SIMULATION
# -----------------------------------

def simulate_restock(
    trend,
    inventory_item
):

    momentum = trend["momentum"]
    confidence = trend["confidence"]

    current_stock = int(
        inventory_item["stock"]
    )

    unit_price = float(
        inventory_item["unit_price"]
    )

    sales_velocity = inventory_item[
        "sales_velocity"
    ].lower()

    category = inventory_item[
        "category"
    ].lower()

    velocity_multiplier = SALES_VELOCITY_MAP.get(
        sales_velocity,
        1.0
    )

    seasonal_multiplier = SEASONAL_MULTIPLIERS.get(
        category,
        1.0
    )

    demand_window = trend.get(
        "peak_prediction_days",
        14
    )

    recommended_stock = int(
        (
            momentum *
            confidence *
            velocity_multiplier *
            seasonal_multiplier *
            demand_window
        ) * 4
    )

    missing_units = max(
        recommended_stock - current_stock,
        0
    )

    estimated_revenue_gain = (
        missing_units *
        unit_price
    )

    estimated_cost = (
        missing_units *
        (unit_price * 0.55)
    )

    estimated_roi = (
        (
            estimated_revenue_gain -
            estimated_cost
        ) / max(estimated_cost, 1)
    ) * 100

    sellout_probability = (
        simulate_sellout_probability(
            momentum,
            confidence,
            current_stock,
            recommended_stock
        )
    )

    risk = "LOW"

    if sellout_probability >= 0.75:
        risk = "CRITICAL"

    elif sellout_probability >= 0.55:
        risk = "HIGH"

    elif sellout_probability >= 0.35:
        risk = "MEDIUM"

    return {
        "product": inventory_item["product_name"],
        "trend": trend["trend"],
        "recommended_restock": recommended_stock,
        "missing_units": missing_units,
        "estimated_revenue_gain": round(
            estimated_revenue_gain,
            2
        ),
        "estimated_roi": round(
            estimated_roi,
            2
        ),
        "sellout_probability": sellout_probability,
        "risk": risk
    }


# -----------------------------------
# OVERSTOCK RISK SIMULATION
# -----------------------------------

def simulate_overstock_risk(
    trend,
    inventory_item
):

    momentum = trend["momentum"]

    current_stock = int(
        inventory_item["stock"]
    )

    unit_price = float(
        inventory_item["unit_price"]
    )

    recommended_stock = int(
        momentum * 40
    )

    excess_units = max(
        current_stock - recommended_stock,
        0
    )

    holding_cost = (
        excess_units *
        (unit_price * 0.18)
    )

    markdown_probability = min(
        0.95,
        excess_units / max(
            recommended_stock,
            1
        )
    )

    dead_inventory_risk = (
        markdown_probability *
        holding_cost
    )

    return {
        "product": inventory_item["product_name"],
        "trend": trend["trend"],
        "excess_units": excess_units,
        "holding_cost": round(
            holding_cost,
            2
        ),
        "markdown_probability": round(
            markdown_probability,
            2
        ),
        "dead_inventory_risk": round(
            dead_inventory_risk,
            2
        )
    }


# -----------------------------------
# PROFIT CHANGE SIMULATION
# -----------------------------------

def simulate_profit_change(
    revenue_gain,
    current_profit_margin=0.35
):

    estimated_profit_delta = (
        revenue_gain *
        current_profit_margin
    )

    margin_improvement = (
        current_profit_margin * 100
    ) * 0.12

    return {
        "profit_delta": round(
            estimated_profit_delta,
            2
        ),
        "margin_improvement": round(
            margin_improvement,
            2
        )
    }