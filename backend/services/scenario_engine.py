import math

from backend.ml.forecasting_engine import (
    forecasting_engine
)

from backend.services.explainability_engine import (
    generate_recommendation_explanation,
    generate_confidence_explanation,
    generate_financial_explanation,
    generate_risk_explanation,
    generate_agent_decision_trace
)

from backend.services.temporal_analysis import (
    calculate_momentum_acceleration
)


# -----------------------------------
# INITIALIZE ML FORECASTING ENGINE
# -----------------------------------

forecasting_engine.run_pipeline()


# -----------------------------------
# SALES VELOCITY MULTIPLIERS
# -----------------------------------

SALES_VELOCITY_MAP = {

    "low": 0.75,

    "medium": 1.0,

    "high": 1.45
}


# -----------------------------------
# CATEGORY SEASONAL WEIGHTS
# -----------------------------------

SEASONAL_MULTIPLIERS = {

    "tops": 1.2,

    "outerwear": 1.35,

    "blazers": 1.15,

    "pants": 0.9,

    "knitwear": 1.1,

    "bottoms": 0.95
}


# -----------------------------------
# ML-POWERED DEMAND PREDICTION
# -----------------------------------

def predict_inventory_demand(
    trend_score,
    stock,
    unit_price,
    sales_velocity
):

    velocity_map = {
        "low": 1,
        "medium": 2,
        "high": 3
    }

    velocity_encoded = (
        velocity_map.get(
            sales_velocity.lower(),
            2
        )
    )

    estimated_units_sold = (
        stock * velocity_encoded
    )

    prediction = (
        forecasting_engine
        .predict_future_demand(
            {
                "trend_score": trend_score,
                "units_sold": estimated_units_sold,
                "unit_price": unit_price,
                "stock": stock,
                "sales_velocity_encoded":
                    velocity_encoded
            }
        )
    )

    return prediction


# -----------------------------------
# TREND STRENGTH SCORE
# -----------------------------------

def calculate_trend_strength(
    momentum,
    confidence
):

    trend_strength = (
        momentum * 0.6
        +
        confidence * 0.4
    )

    return round(
        trend_strength,
        2
    )


# -----------------------------------
# SELL OUT PROBABILITY
# -----------------------------------

def simulate_sellout_probability(

    momentum,
    confidence,
    current_stock,
    recommended_stock

):

    demand_strength = (
        momentum *
        confidence
    )

    stock_coverage = (
        current_stock /
        max(recommended_stock, 1)
    )

    probability = (
        demand_strength *
        (1 - min(stock_coverage, 1))
    )

    probability = max(
        0.05,
        min(probability, 0.95)
    )

    return round(
        probability,
        2
    )


# -----------------------------------
# INVENTORY HEALTH SCORE
# -----------------------------------

def calculate_inventory_health_score(

    sellout_probability,
    overstock_probability

):

    health_score = (
        (
            sellout_probability * 100
        )
        -
        (
            overstock_probability * 100
        )
    )

    health_score = max(
        0,
        min(health_score, 100)
    )

    return round(
        health_score,
        2
    )


# -----------------------------------
# RESTOCK SIMULATION
# -----------------------------------

def simulate_restock(

    trend,
    inventory_item

):

    # -----------------------------------
    # INPUT VARIABLES
    # -----------------------------------

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

    demand_window = trend.get(
        "peak_prediction_days",
        14
    )

    # -----------------------------------
    # MULTIPLIERS
    # -----------------------------------

    velocity_multiplier = (
        SALES_VELOCITY_MAP.get(
            sales_velocity,
            1.0
        )
    )

    seasonal_multiplier = (
        SEASONAL_MULTIPLIERS.get(
            category,
            1.0
        )
    )

    trend_strength = (
        calculate_trend_strength(
            momentum,
            confidence
        )
    )

    # -----------------------------------
    # TEMPORAL INTELLIGENCE
    # -----------------------------------

    temporal_data = (
        calculate_momentum_acceleration(

            trend["trend"],
            momentum

        )
    )

    # -----------------------------------
    # DEMAND FORECAST
    # -----------------------------------

    # Calculate trend score for ML model
    trend_score = int(
        trend_strength * 100
    )

    # Use ML forecasting for predicted demand
    predicted_future_demand = (
        predict_inventory_demand(
            trend_score=trend_score,
            stock=current_stock,
            unit_price=unit_price,
            sales_velocity=sales_velocity
        )
    )

    # Recommended restock based on ML prediction
    recommended_restock = max(
        int(predicted_future_demand - current_stock),
        0
    )

    target_inventory = (
        current_stock +
        recommended_restock
    )

    # Project demand for temporal analysis
    projected_demand = int(
        predicted_future_demand
    )

    # -----------------------------------
    # REVENUE FORECAST
    # -----------------------------------

    estimated_revenue_gain = (

        recommended_restock *
        unit_price

    )

    estimated_cost = (

        recommended_restock *
        (
            unit_price * 0.55
        )

    )

    estimated_profit = (
        estimated_revenue_gain
        -
        estimated_cost
    )

    estimated_roi = (

        estimated_profit
        /
        max(estimated_cost, 1)

    ) * 100

    # -----------------------------------
    # SELL OUT FORECAST
    # -----------------------------------

    sellout_probability = (
        simulate_sellout_probability(

            momentum,
            confidence,
            current_stock,
            target_inventory
        )
    )

    # -----------------------------------
    # STOCKOUT RISK
    # -----------------------------------

    stockout_risk = "LOW"

    if sellout_probability >= 0.75:

        stockout_risk = "CRITICAL"

    elif sellout_probability >= 0.55:

        stockout_risk = "HIGH"

    elif sellout_probability >= 0.35:

        stockout_risk = "MEDIUM"

    # -----------------------------------
    # INVENTORY RISK
    # -----------------------------------

    inventory_risk = "LOW"

    if sellout_probability <= 0.2:

        inventory_risk = "HIGH"

    elif sellout_probability <= 0.45:

        inventory_risk = "MEDIUM"

    # -----------------------------------
    # OVERSTOCK PROBABILITY
    # -----------------------------------

    overstock_probability = max(

        0.05,

        round(
            (
                target_inventory
                -
                projected_demand
            )
            /
            max(target_inventory, 1),

            2
        )
    )

    # -----------------------------------
    # INVENTORY HEALTH SCORE
    # -----------------------------------

    inventory_health_score = (
        calculate_inventory_health_score(

            sellout_probability,
            overstock_probability
        )
    )

    # -----------------------------------
    # DEMAND LABEL
    # -----------------------------------

    demand_label = "STABLE"

    if momentum >= 0.85:

        demand_label = "EXPLOSIVE"

    elif momentum >= 0.7:

        demand_label = "ACCELERATING"

    elif momentum <= 0.45:

        demand_label = "DECLINING"

    # -----------------------------------
    # BASE SIMULATION RESULT
    # -----------------------------------

    simulation_result = {

        "product":
        inventory_item["product_name"],

        "category":
        category,

        "trend":
        trend["trend"],

        "trend_strength":
        trend_strength,

        "predicted_future_demand":
        round(predicted_future_demand, 2),

        "recommended_restock":
        recommended_restock,

        "target_inventory":
        target_inventory,

        "projected_demand":
        projected_demand,

        "missing_units":
        recommended_restock,

        "estimated_revenue_gain":
        round(
            estimated_revenue_gain,
            2
        ),

        "estimated_profit":
        round(
            estimated_profit,
            2
        ),

        "estimated_roi":
        round(
            estimated_roi,
            2
        ),

        "sellout_probability":
        sellout_probability,

        "overstock_probability":
        overstock_probability,

        "inventory_health_score":
        inventory_health_score,

        "stockout_risk":
        stockout_risk,

        "inventory_risk":
        inventory_risk,

        "demand_label":
        demand_label
    }

    # -----------------------------------
    # EXPLAINABILITY LAYER
    # -----------------------------------

    recommendation_explanation = (
        generate_recommendation_explanation(

            trend,
            simulation_result,
            temporal_data
        )
    )

    confidence_explanation = (
        generate_confidence_explanation(

            trend,
            temporal_data,
            simulation_result
        )
    )

    financial_explanation = (
        generate_financial_explanation(
            simulation_result
        )
    )

    risk_explanation = (
        generate_risk_explanation(

            simulation_result,
            temporal_data
        )
    )

    decision_trace = (
        generate_agent_decision_trace(

            trend,
            simulation_result,
            temporal_data
        )
    )

    # -----------------------------------
    # ATTACH EXPLAINABILITY
    # -----------------------------------

    simulation_result[
        "decision_explanation"
    ] = recommendation_explanation

    simulation_result[
        "confidence_explanation"
    ] = confidence_explanation

    simulation_result[
        "financial_rationale"
    ] = financial_explanation

    simulation_result[
        "risk_rationale"
    ] = risk_explanation

    simulation_result[
        "decision_trace"
    ] = decision_trace

    # -----------------------------------
    # FINAL RESULT
    # -----------------------------------

    return simulation_result


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
        momentum * 45
    )

    excess_units = max(

        current_stock
        -
        recommended_stock,

        0
    )

    holding_cost = (

        excess_units *
        (
            unit_price * 0.18
        )

    )

    markdown_probability = min(

        0.95,

        excess_units /
        max(recommended_stock, 1)

    )

    dead_inventory_risk = (

        markdown_probability *
        holding_cost

    )

    # -----------------------------------
    # RISK CLASSIFICATION
    # -----------------------------------

    risk_level = "LOW"

    if markdown_probability >= 0.7:

        risk_level = "HIGH"

    elif markdown_probability >= 0.4:

        risk_level = "MEDIUM"

    # -----------------------------------
    # INVENTORY EXPOSURE SCORE
    # -----------------------------------

    inventory_exposure_score = round(

        (
            markdown_probability * 100
        )
        +
        (
            excess_units * 0.3
        ),

        2
    )

    return {

        "product":
        inventory_item["product_name"],

        "trend":
        trend["trend"],

        "recommended_stock":
        recommended_stock,

        "excess_units":
        excess_units,

        "holding_cost":
        round(
            holding_cost,
            2
        ),

        "markdown_probability":
        round(
            markdown_probability,
            2
        ),

        "dead_inventory_risk":
        round(
            dead_inventory_risk,
            2
        ),

        "inventory_exposure_score":
        inventory_exposure_score,

        "risk_level":
        risk_level
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

    projected_margin = (

        current_profit_margin * 100
        +
        margin_improvement

    )

    return {

        "profit_delta":
        round(
            estimated_profit_delta,
            2
        ),

        "margin_improvement":
        round(
            margin_improvement,
            2
        ),

        "projected_margin":
        round(
            projected_margin,
            2
        )
    }