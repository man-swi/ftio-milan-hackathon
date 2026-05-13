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

        response_rules = (
            build_response_rules()
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
        INVENTORY SNAPSHOT
        ===================================

        {inventory_summary}

        ===================================
        TEMPORAL TREND MEMORY
        ===================================

        {memory_summary}

        ===================================
        RETAIL KNOWLEDGE
        ===================================

        {retrieved_context}

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