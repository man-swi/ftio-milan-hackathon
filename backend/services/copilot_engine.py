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
    inventory_df
):

    inventory_summary = []

    for row in inventory_df.to_dict(
        orient="records"
    ):

        inventory_summary.append(

            f"""
            Product: {row['product_name']}
            Category: {row['category']}
            Stock: {row['stock']}
            Sales Velocity: {row['sales_velocity']}
            Unit Price: {row['unit_price']}
            """
        )

    return "\n".join(
        inventory_summary
    )


# -----------------------------------
# BUILD TEMPORAL MEMORY SUMMARY
# -----------------------------------

def build_memory_summary(
    historical_trends
):

    if not historical_trends:

        return "No historical trend memory available."

    memory_lines = []

    for trend in historical_trends:

        memory_lines.append(

            f"""
            Trend: {trend['trend_name']}
            Momentum: {trend['momentum']}
            Recorded At: {trend['recorded_at']}
            """
        )

    return "\n".join(
        memory_lines
    )


# -----------------------------------
# BUILD SCENARIO SUMMARIES
# -----------------------------------

def build_simulation_summary(
    trend_data,
    inventory_df
):

    simulation_outputs = []

    inventory_records = inventory_df.to_dict(
        orient="records"
    )

    for trend, item in zip(
        trend_data,
        inventory_records
    ):

        restock_result = simulate_restock(
            trend,
            item
        )

        overstock_result = (
            simulate_overstock_risk(
                trend,
                item
            )
        )

        profit_result = (
            simulate_profit_change(
                trend,
                item
            )
        )

        simulation_outputs.append(

            f"""
            Product: {item['product_name']}

            Recommended Restock:
            {restock_result['recommended_restock']}

            Revenue Gain:
            {restock_result['estimated_revenue_gain']}

            Sellout Probability:
            {restock_result['sellout_probability']}

            Risk Level:
            {restock_result['risk']}

            Overstock Risk:
            {overstock_result['risk_level']}

            Profit Delta:
            {profit_result['profit_delta']}
            """
        )

    return "\n".join(
        simulation_outputs
    )


# -----------------------------------
# BUILD COPILOT RESPONSE
# -----------------------------------

def generate_copilot_response(
    user_query
):

    # -----------------------------------
    # LOAD CURRENT DATA
    # -----------------------------------

    trend_data = load_mock_trends()

    inventory_df = load_inventory()

    # -----------------------------------
    # BUSINESS METRICS
    # -----------------------------------

    business_metrics = (
        calculate_business_metrics(
            trend_data,
            inventory_df
        )
    )

    # -----------------------------------
    # RETRIEVAL CONTEXT
    # -----------------------------------

    retrieved_context = retrieve_context(
        user_query
    )

    # -----------------------------------
    # TEMPORAL MEMORY
    # -----------------------------------

    historical_trends = (
        get_historical_trends()
    )

    memory_summary = (
        build_memory_summary(
            historical_trends
        )
    )

    # -----------------------------------
    # INVENTORY CONTEXT
    # -----------------------------------

    inventory_context = (
        build_inventory_summary(
            inventory_df
        )
    )

    # -----------------------------------
    # SCENARIO SIMULATION CONTEXT
    # -----------------------------------

    simulation_context = (
        build_simulation_summary(
            trend_data,
            inventory_df
        )
    )

    # -----------------------------------
    # PROMPT
    # -----------------------------------

    prompt = f"""

    You are FTIO.

    FTIO is an enterprise-grade
    AI Retail Copilot.

    Your job is to help fashion executives make:

    - inventory decisions
    - merchandising decisions
    - pricing decisions
    - retail strategy decisions
    - risk management decisions

    ===================================
    USER QUESTION
    ===================================

    {user_query}

    ===================================
    BUSINESS METRICS
    ===================================

    Revenue Opportunity:
    {business_metrics['total_revenue_opportunity']}

    Inventory Risk:
    {business_metrics['total_inventory_risk']}

    Average Confidence:
    {business_metrics['average_confidence']}

    ===================================
    CURRENT INVENTORY
    ===================================

    {inventory_context}

    ===================================
    HISTORICAL TREND MEMORY
    ===================================

    {memory_summary}

    ===================================
    RETRIEVED RETAIL KNOWLEDGE
    ===================================

    {retrieved_context}

    ===================================
    BUSINESS SIMULATION INSIGHTS
    ===================================

    {simulation_context}

    ===================================
    RESPONSE INSTRUCTIONS
    ===================================

    Your response must:

    - sound like an executive retail advisor
    - provide strategic reasoning
    - explain business implications
    - reference inventory risks
    - mention trend acceleration when relevant
    - use retrieval context when useful
    - mention simulation outcomes when useful

    Avoid:

    - generic chatbot responses
    - short vague answers
    - unnecessary repetition
    - hallucinated numbers

    Keep answers:

    - professional
    - data-driven
    - strategic
    - concise but insightful

    """

    # -----------------------------------
    # GENERATE RESPONSE
    # -----------------------------------

    try:

        response = generate_groq_response(
            prompt
        )

        return response

    except Exception as error:

        return f"Copilot Error: {str(error)}"