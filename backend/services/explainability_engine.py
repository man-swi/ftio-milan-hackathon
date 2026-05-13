# ===================================
# FTIO EXPLAINABILITY ENGINE
# ===================================

from typing import Dict, List


# ===================================
# RECOMMENDATION EXPLANATION
# ===================================

def generate_recommendation_explanation(
    trend: Dict,
    simulation: Dict,
    temporal_data: Dict
):

    explanations = []

    momentum_change = temporal_data.get(
        "momentum_change",
        0
    )

    # -----------------------------------
    # MOMENTUM REASONING
    # -----------------------------------

    if momentum_change > 0:

        explanations.append(

            f"Trend momentum increased "
            f"{momentum_change}%"

        )

    elif momentum_change < 0:

        explanations.append(

            f"Trend momentum declined "
            f"{abs(momentum_change)}%"

        )

    # -----------------------------------
    # DEMAND REASONING
    # -----------------------------------

    if simulation["recommended_restock"] > 0:

        explanations.append(

            "Current inventory is below "
            "projected demand levels"

        )

    # -----------------------------------
    # SELLOUT REASONING
    # -----------------------------------

    sellout_probability = int(
        simulation["sellout_probability"] * 100
    )

    explanations.append(

        f"Sellout probability reached "
        f"{sellout_probability}%"

    )

    # -----------------------------------
    # DEMAND LABEL
    # -----------------------------------

    explanations.append(

        f"Demand classified as "
        f"{simulation['demand_label']}"

    )

    return {

        "recommendation":
        f"Restock {simulation['product']}",

        "why":
        explanations
    }


# ===================================
# CONFIDENCE EXPLANATION
# ===================================

def generate_confidence_explanation(
    trend: Dict,
    temporal_data: Dict,
    simulation: Dict
):

    confidence = trend.get(
        "confidence",
        0
    )

    confidence_factors = []

    # -----------------------------------
    # TREND CONFIDENCE
    # -----------------------------------

    if confidence >= 0.85:

        confidence_factors.append(
            "High trend confidence"
        )

    elif confidence >= 0.7:

        confidence_factors.append(
            "Moderate trend consistency"
        )

    else:

        confidence_factors.append(
            "Trend confidence weakening"
        )

    # -----------------------------------
    # VOLATILITY ANALYSIS
    # -----------------------------------

    volatility = temporal_data.get(
        "volatility_score",
        0
    )

    if volatility <= 10:

        confidence_factors.append(
            "Low volatility detected"
        )

    elif volatility <= 25:

        confidence_factors.append(
            "Moderate volatility detected"
        )

    else:

        confidence_factors.append(
            "High volatility reducing confidence"
        )

    # -----------------------------------
    # INVENTORY HEALTH
    # -----------------------------------

    health_score = simulation.get(
        "inventory_health_score",
        0
    )

    if health_score >= 70:

        confidence_factors.append(
            "Strong inventory alignment"
        )

    elif health_score >= 40:

        confidence_factors.append(
            "Moderate inventory positioning"
        )

    else:

        confidence_factors.append(
            "Weak inventory positioning"
        )

    return {

        "confidence":
        round(confidence, 2),

        "confidence_factors":
        confidence_factors
    }


# ===================================
# FINANCIAL EXPLANATION
# ===================================

def generate_financial_explanation(
    simulation: Dict
):

    revenue_gain = simulation.get(
        "estimated_revenue_gain",
        0
    )

    roi = simulation.get(
        "estimated_roi",
        0
    )

    projected_demand = simulation.get(
        "projected_demand",
        0
    )

    recommended_restock = simulation.get(
        "recommended_restock",
        0
    )

    financial_reasoning = [

        f"Projected demand estimated "
        f"at {projected_demand} units",

        f"Recommended restock quantity "
        f"is {recommended_restock} units",

        f"Estimated revenue gain "
        f"is ${revenue_gain:,.0f}",

        f"Projected ROI estimated "
        f"at {roi}%"
    ]

    return {

        "estimated_revenue_gain":
        revenue_gain,

        "estimated_roi":
        roi,

        "financial_reasoning":
        financial_reasoning
    }


# ===================================
# RISK EXPLANATION
# ===================================

def generate_risk_explanation(
    simulation: Dict,
    temporal_data: Dict
):

    risk_reasons = []

    stockout_risk = simulation.get(
        "stockout_risk",
        "LOW"
    )

    inventory_risk = simulation.get(
        "inventory_risk",
        "LOW"
    )

    volatility_score = temporal_data.get(
        "volatility_score",
        0
    )

    # -----------------------------------
    # STOCKOUT RISK
    # -----------------------------------

    if stockout_risk in [

        "HIGH",
        "CRITICAL"

    ]:

        risk_reasons.append(

            "Elevated stockout probability "
            "detected"

        )

    # -----------------------------------
    # INVENTORY RISK
    # -----------------------------------

    if inventory_risk == "HIGH":

        risk_reasons.append(

            "Inventory exposure risk increasing"

        )

    elif inventory_risk == "MEDIUM":

        risk_reasons.append(

            "Moderate inventory imbalance detected"

        )

    # -----------------------------------
    # VOLATILITY
    # -----------------------------------

    if volatility_score > 25:

        risk_reasons.append(

            "Trend volatility remains elevated"

        )

    # -----------------------------------
    # DEFAULT SAFE STATE
    # -----------------------------------

    if not risk_reasons:

        risk_reasons.append(

            "No major operational risks detected"

        )

    return {

        "risk_level":
        inventory_risk,

        "risk_reasons":
        risk_reasons
    }


# ===================================
# AGENT DECISION TRACE
# ===================================

def generate_agent_decision_trace(
    trend: Dict,
    simulation: Dict,
    temporal_data: Dict
):

    trace = [

        {

            "agent":
            "Trend Agent",

            "decision":
            f"Detected {trend['trend']} momentum",

            "evidence":
            f"Momentum score: "
            f"{trend['momentum']}"
        },

        {

            "agent":
            "Temporal Intelligence Engine",

            "decision":
            "Analyzed trend acceleration",

            "evidence":
            f"Momentum change: "
            f"{temporal_data['momentum_change']}%"
        },

        {

            "agent":
            "Inventory Agent",

            "decision":
            "Detected inventory imbalance",

            "evidence":
            f"Recommended restock: "
            f"{simulation['recommended_restock']}"
        },

        {

            "agent":
            "Scenario Engine",

            "decision":
            "Simulated retail outcomes",

            "evidence":
            f"Sellout probability: "
            f"{int(simulation['sellout_probability'] * 100)}%"
        },

        {

            "agent":
            "Risk Engine",

            "decision":
            "Evaluated operational exposure",

            "evidence":
            f"Inventory risk: "
            f"{simulation['inventory_risk']}"
        }
    ]

    return trace[:4]


# ===================================
# FULL EXECUTIVE EXPLAINABILITY
# ===================================

def generate_executive_explanation(
    trend: Dict,
    simulation: Dict,
    temporal_data: Dict
):

    recommendation = (
        generate_recommendation_explanation(

            trend,
            simulation,
            temporal_data
        )
    )

    confidence = (
        generate_confidence_explanation(

            trend,
            temporal_data,
            simulation
        )
    )

    financials = (
        generate_financial_explanation(
            simulation
        )
    )

    risks = (
        generate_risk_explanation(

            simulation,
            temporal_data
        )
    )

    trace = (
        generate_agent_decision_trace(

            trend,
            simulation,
            temporal_data
        )
    )

    return {

        "recommendation":
        recommendation,

        "confidence":
        confidence,

        "financials":
        financials,

        "risks":
        risks,

        "decision_trace":
        trace
    }