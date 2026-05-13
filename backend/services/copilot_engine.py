from backend.services.rag_engine import (
    retrieve_context
)

from backend.services.memory_engine import (
    get_historical_trends
)

from backend.services.business_metrics import (
    calculate_business_metrics
)

from backend.services.scenario_engine import (
    simulate_restock,
    simulate_overstock_risk,
    simulate_profit_change
)

from backend.tools.load_trends import (
    load_mock_trends
)

from backend.tools.load_inventory import (
    load_inventory
)

from backend.agents.base import (
    generate_groq_response
)


# -----------------------------------
# TOKEN BUDGET CONSTANTS
# -----------------------------------

TOKEN_BUDGET = {
    "max_simulations":      3,
    "max_evidence_chains":  3,
    "max_traces":           2,
    "max_alerts":           2,
}


# -----------------------------------
# BUILD INVENTORY SUMMARY
# -----------------------------------

def build_inventory_summary(
    inventory_data
):

    summary = []

    for item in inventory_data:

        summary.append({

            "product":
            item["product_name"],

            "category":
            item["category"],

            "stock":
            item["stock"],

            "velocity":
            item["sales_velocity"],

            "price":
            item["unit_price"]
        })

    return summary


# -----------------------------------
# BUILD MEMORY SUMMARY
# -----------------------------------

def build_memory_summary(
    historical_trends
):

    if not historical_trends:

        return []

    memory_summary = []

    for trend in historical_trends[:6]:

        memory_summary.append({

            "trend":
            trend["trend_name"],

            "momentum":
            trend["momentum"],

            "recorded_at":
            trend["recorded_at"]
        })

    return memory_summary


# -----------------------------------
# BUILD EXECUTIVE SIMULATION SUMMARY
# -----------------------------------

def build_simulation_summary(
    trend_data,
    inventory_data
):

    simulations = []

    for trend in trend_data:

        for item in inventory_data:

            if (
                item["category"].lower()
                !=
                trend["category"].lower()
            ):

                continue

            restock = simulate_restock(
                trend,
                item
            )

            overstock = (
                simulate_overstock_risk(
                    trend,
                    item
                )
            )

            profit = (
                simulate_profit_change(
                    restock[
                        "estimated_revenue_gain"
                    ]
                )
            )

            simulations.append({

                "product":
                item["product_name"],

                "category":
                item["category"],

                "trend":
                trend["trend"],

                "restock":
                restock[
                    "recommended_restock"
                ],

                "revenue":
                restock[
                    "estimated_revenue_gain"
                ],

                "sellout_probability":
                restock[
                    "sellout_probability"
                ],

                "stockout_risk":
                restock[
                    "stockout_risk"
                ],

                "inventory_risk":
                restock[
                    "inventory_risk"
                ],

                "overstock_risk":
                overstock[
                    "risk_level"
                ],

                "profit_delta":
                profit[
                    "profit_delta"
                ],

                "momentum":
                trend["momentum"]
            })

    # -----------------------------------
    # SORT BY REVENUE OPPORTUNITY
    # -----------------------------------

    simulations = sorted(

        simulations,

        key=lambda x:
        x["revenue"],

        reverse=True
    )

    # -----------------------------------
    # KEEP ONLY TOP EXECUTIVE INSIGHTS
    # -----------------------------------

    return simulations[:5]


# -----------------------------------
# BUILD EXECUTIVE PRIORITIES
# -----------------------------------

def build_executive_priorities(
    simulations
):

    priorities = []

    for sim in simulations:

        priorities.append(

            f"""
            Product:
            {sim['product']}

            Revenue:
            ${sim['revenue']}

            Sellout:
            {round(sim['sellout_probability'] * 100)}%

            Inventory Risk:
            {sim['inventory_risk']}

            Trend:
            {sim['trend']}
            """
        )

    return "\n".join(
        priorities
    )


# -----------------------------------
# BUILD COMPRESSED COPILOT CONTEXT
# -----------------------------------

def build_compressed_copilot_context(
    simulation_summary,
    memory_summary,
    business_metrics
):

    return {

        "top_opportunities": [
            {
                "product": s["product"],
                "revenue": s["revenue"],
                "trend": s["trend"],
                "sellout_probability": (
                    f"{round(s['sellout_probability'] * 100)}%"
                )
            }
            for s in simulation_summary[:3]
        ],

        "top_risks": [
            {
                "product": s["product"],
                "inventory_risk": s["inventory_risk"],
                "overstock_risk": s["overstock_risk"]
            }
            for s in simulation_summary
            if s["inventory_risk"] in [
                "High", "Critical"
            ]
        ][:3],

        "top_consensus": {
            "revenue_opportunity": (
                business_metrics[
                    "total_revenue_opportunity"
                ]
            ),
            "inventory_risk": (
                business_metrics[
                    "total_inventory_risk"
                ]
            ),
            "confidence": (
                business_metrics[
                    "average_confidence"
                ]
            )
        },

        "key_trends": [
            {
                "trend": m["trend"],
                "momentum": m["momentum"]
            }
            for m in memory_summary[:3]
        ]
    }


# -----------------------------------
# BUILD RESPONSE STYLE RULES
# -----------------------------------

def build_response_rules():

    return """

    RESPONSE STYLE RULES

    Your response MUST:

    - sound like a senior retail strategist
    - prioritize executive clarity
    - use concise business language
    - avoid repetitive explanations
    - avoid repeating trend names excessively
    - avoid repeating inventory risk terminology
    - avoid generic AI phrasing

    RESPONSE STRUCTURE:

    1. Executive Summary
    - 2-3 sentence overview

    2. Top Priorities
    - maximum 3 bullets
    - ranked by revenue impact

    3. Risk Signals
    - short concise section

    4. Strategic Action
    - final recommendation

    IMPORTANT:

    - Keep response under 500 words
    - Do NOT repeat the same insight twice
    - Compress repetitive simulation details
    - Mention only highest-impact products
    - Focus on decisions, not descriptions
    - Avoid long introductions
    - Avoid unnecessary trend storytelling
    """


# -----------------------------------
# STEP 4 — TOKEN BUDGETING
# Limits evidence chains, traces,
# simulations, and alerts before
# they are injected into the prompt.
# -----------------------------------

def apply_token_budget(
    simulation_summary,
    retrieved_context,
    memory_summary,
    executive_priorities_list
):

    # --- Limit simulations ---
    # Keep only the top N simulations
    # ranked by revenue (already sorted).
    budgeted_simulations = (
        simulation_summary[
            :TOKEN_BUDGET["max_simulations"]
        ]
    )

    # --- Limit evidence chains ---
    # RAG context is treated as a list of
    # evidence chunks. Slice to max allowed.
    if isinstance(retrieved_context, list):
        budgeted_evidence = (
            retrieved_context[
                :TOKEN_BUDGET["max_evidence_chains"]
            ]
        )
    else:
        # If context is a raw string, split
        # by double-newline and re-join after
        # slicing to the allowed limit.
        evidence_chunks = [
            chunk.strip()
            for chunk in retrieved_context.split("\n\n")
            if chunk.strip()
        ]
        budgeted_evidence = "\n\n".join(
            evidence_chunks[
                :TOKEN_BUDGET["max_evidence_chains"]
            ]
        )

    # --- Limit traces ---
    # Memory trends act as historical
    # traces. Cap at max_traces.
    budgeted_traces = (
        memory_summary[
            :TOKEN_BUDGET["max_traces"]
        ]
    )

    # --- Limit alerts ---
    # Executive priorities act as alerts.
    # Keep only the top N by revenue impact.
    budgeted_alerts = (
        executive_priorities_list[
            :TOKEN_BUDGET["max_alerts"]
        ]
    )

    return (
        budgeted_simulations,
        budgeted_evidence,
        budgeted_traces,
        budgeted_alerts
    )


# -----------------------------------
# GENERATE COPILOT RESPONSE
# -----------------------------------

def generate_copilot_response(
    user_query
):

    try:

        print("STEP 1")

        trend_data = (
            load_mock_trends()
        )

        print("STEP 2")

        inventory_data = (
            load_inventory()
        )

        print("STEP 3")

        business_metrics = (
            calculate_business_metrics(
                trend_data,
                inventory_data
            )
        )

        print("STEP 4")

        retrieved_context = (
            retrieve_context(
                user_query
            )
        )

        print("STEP 5")

        historical_trends = (
            get_historical_trends()
        )

        print("STEP 6")

        inventory_summary = (
            build_inventory_summary(
                inventory_data
            )
        )

        print("STEP 7")

        memory_summary = (
            build_memory_summary(
                historical_trends
            )
        )

        print("STEP 8")

        simulation_summary = (
            build_simulation_summary(
                trend_data,
                inventory_data
            )
        )

        print("STEP 9")

        executive_priorities = (
            build_executive_priorities(
                simulation_summary
            )
        )

        print("STEP 10")

        compressed_context = (
            build_compressed_copilot_context(
                simulation_summary,
                memory_summary,
                business_metrics
            )
        )

        response_rules = (
            build_response_rules()
        )

        # -----------------------------------
        # STEP 4 — APPLY TOKEN BUDGETING
        # Trim all prompt inputs before
        # injection to stay within limits.
        # -----------------------------------

        print("STEP 4 — TOKEN BUDGETING")

        executive_priorities_list = (
            simulation_summary
        )

        (
            budgeted_simulations,
            budgeted_evidence,
            budgeted_traces,
            budgeted_alerts
        ) = apply_token_budget(
            simulation_summary,
            retrieved_context,
            memory_summary,
            executive_priorities_list
        )

        # Rebuild compressed context and
        # executive priorities from the
        # budgeted (trimmed) data only.

        compressed_context = (
            build_compressed_copilot_context(
                budgeted_simulations,
                budgeted_traces,
                business_metrics
            )
        )

        executive_priorities = (
            build_executive_priorities(
                budgeted_alerts
            )
        )

        # -----------------------------------
        # EXECUTIVE PROMPT
        # -----------------------------------

        prompt = f"""

        You are FTIO.

        FTIO is an enterprise AI retail
        strategy copilot for fashion executives.

        ===================================
        USER QUESTION
        ===================================

        {user_query}

        ===================================
        BUSINESS METRICS
        ===================================

        Revenue Opportunity:
        ${business_metrics['total_revenue_opportunity']}

        Inventory Risk:
        ${business_metrics['total_inventory_risk']}

        Average Confidence:
        {business_metrics['average_confidence']}

        ===================================
        EXECUTIVE PRIORITIES
        ===================================

        {executive_priorities}

        ===================================
        COMPRESSED EXECUTIVE CONTEXT
        ===================================

        {compressed_context}

        ===================================
        RETAIL KNOWLEDGE
        ===================================

        {budgeted_evidence}

        ===================================
        RESPONSE RULES
        ===================================

        {response_rules}

        """

        print("STEP 11")

        response = (
            generate_groq_response(
                prompt
            )
        )

        print("STEP 12")

        return response

    except Exception as error:

        print("COPILOT ERROR:")

        print(str(error))

        return (
            f"Copilot Error: {str(error)}"
        )