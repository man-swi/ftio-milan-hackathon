# ===================================
# FTIO CONSENSUS ENGINE
# ===================================

from typing import Dict, List


# ===================================
# CONSENSUS SCORE
# ===================================

def calculate_consensus_score(
    confidence: float,
    trend_strength: float,
    sellout_probability: float,
    volatility_score: float
):

    score = (

        (confidence * 0.35) +

        (trend_strength * 0.30) +

        (sellout_probability * 0.25) -

        ((volatility_score / 100) * 0.10)

    )

    return round(
        max(0, min(score, 1)),
        2
    )


# ===================================
# RISK OVERRIDE LOGIC
# ===================================

def evaluate_risk_override(
    inventory_risk: str,
    volatility_score: float
):

    if inventory_risk in [

        "HIGH",
        "CRITICAL"

    ]:

        return {

            "override": True,

            "reason":
            "Inventory exposure risk exceeded threshold"
        }

    if volatility_score >= 30:

        return {

            "override": True,

            "reason":
            "Trend volatility too unstable"
        }

    return {

        "override": False,

        "reason":
        "No critical override conditions detected"
    }


# ===================================
# SUPPORTING EVIDENCE
# ===================================

def build_supporting_evidence(
    explanation: Dict,
    financials: Dict,
    risks: Dict
):

    evidence = []

    # -----------------------------------
    # RECOMMENDATION WHY
    # -----------------------------------

    for item in explanation.get(
        "why",
        []
    ):

        evidence.append(item)

    # -----------------------------------
    # FINANCIAL REASONING
    # -----------------------------------

    for item in financials.get(
        "financial_reasoning",
        []
    ):

        evidence.append(item)

    # -----------------------------------
    # RISK REASONS
    # -----------------------------------

    for item in risks.get(
        "risk_reasons",
        []
    ):

        evidence.append(item)

    return evidence


# ===================================
# CONFLICT DETECTION
# ===================================

def detect_conflicts(
    risks: Dict,
    confidence: Dict
):

    conflicts = []

    risk_level = risks.get(
        "risk_level",
        "LOW"
    )

    confidence_score = confidence.get(
        "confidence",
        0
    )

    # -----------------------------------
    # HIGH RISK VS HIGH CONFIDENCE
    # -----------------------------------

    if risk_level in [

        "HIGH",
        "CRITICAL"

    ] and confidence_score >= 0.8:

        conflicts.append(

            "High confidence detected despite elevated inventory risk"

        )

    # -----------------------------------
    # LOW CONFIDENCE
    # -----------------------------------

    if confidence_score <= 0.5:

        conflicts.append(

            "Recommendation confidence remains weak"

        )

    return conflicts


# ===================================
# EXECUTIVE CONSENSUS
# ===================================

def generate_consensus_decision(
    simulation_result: Dict,
    temporal_data: Dict
):

    # -----------------------------------
    # LOAD EXPLAINABILITY
    # -----------------------------------

    explanation = simulation_result.get(
        "decision_explanation",
        {}
    )

    confidence = simulation_result.get(
        "confidence_explanation",
        {}
    )

    financials = simulation_result.get(
        "financial_rationale",
        {}
    )

    risks = simulation_result.get(
        "risk_rationale",
        {}
    )

    # -----------------------------------
    # CONSENSUS SCORE
    # -----------------------------------

    consensus_score = (
        calculate_consensus_score(

            confidence.get(
                "confidence",
                0
            ),

            simulation_result.get(
                "trend_strength",
                0
            ),

            simulation_result.get(
                "sellout_probability",
                0
            ),

            temporal_data.get(
                "volatility_score",
                0
            )
        )
    )

    # -----------------------------------
    # RISK OVERRIDE
    # -----------------------------------

    risk_override = (
        evaluate_risk_override(

            simulation_result.get(
                "inventory_risk",
                "LOW"
            ),

            temporal_data.get(
                "volatility_score",
                0
            )
        )
    )

    # -----------------------------------
    # SUPPORTING EVIDENCE
    # -----------------------------------

    evidence_chain = (
        build_supporting_evidence(

            explanation,
            financials,
            risks
        )
    )

    # -----------------------------------
    # CONFLICT ANALYSIS
    # -----------------------------------

    conflicts = (
        detect_conflicts(
            risks,
            confidence
        )
    )

    # -----------------------------------
    # FINAL DECISION
    # -----------------------------------

    if risk_override["override"]:

        final_decision = (

            "Recommendation requires executive review "
            "before operational execution"

        )

    elif consensus_score >= 0.8:

        final_decision = (

            "Recommendation strongly supported "
            "by consensus intelligence"

        )

    elif consensus_score >= 0.6:

        final_decision = (

            "Recommendation moderately supported "
            "with manageable operational risk"

        )

    else:

        final_decision = (

            "Recommendation confidence remains limited"
        )

    # -----------------------------------
    # RETURN CONSENSUS OBJECT
    # -----------------------------------

    return {

        "final_decision":
        final_decision,

        "consensus_score":
        consensus_score,

        "supporting_agents": [

            "Trend Agent",
            "Inventory Agent",
            "Scenario Engine",
            "Risk Engine",
            "Temporal Intelligence Engine"
        ],

        "conflicting_agents":
        conflicts,

        "risk_override":
        risk_override,

        "evidence_chain":
        evidence_chain[:5]
    }