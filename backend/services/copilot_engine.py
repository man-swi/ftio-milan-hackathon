from backend.services.rag_engine import (
    retrieve_context
)

from backend.services.memory_engine import (
    get_historical_trends
)

from backend.services.business_metrics import (
    calculate_business_metrics
)

from backend.tools.load_trends import (
    load_mock_trends
)

from backend.tools.load_inventory import (
    load_inventory
)

from backend.agents.base import groq_llm


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

    business_metrics = (
        calculate_business_metrics(
            trend_data,
            inventory_df
        )
    )

    # -----------------------------------
    # RETRIEVE DOMAIN CONTEXT
    # -----------------------------------

    retrieved_context = retrieve_context(
        user_query
    )

    # -----------------------------------
    # LOAD TEMPORAL MEMORY
    # -----------------------------------

    historical_trends = (
        get_historical_trends()
    )

    # -----------------------------------
    # BUILD INVENTORY SUMMARY
    # -----------------------------------

    inventory_summary = []

    for row in inventory_df.to_dict(
        orient="records"
    ):

        inventory_summary.append(

            f"""
            Product:
            {row['product_name']}

            Category:
            {row['category']}

            Stock:
            {row['stock']}

            Sales Velocity:
            {row['sales_velocity']}
            """
        )

    inventory_context = "\n".join(
        inventory_summary
    )

    # -----------------------------------
    # BUILD PROMPT
    # -----------------------------------

    prompt = f"""

    You are FTIO,
    an AI retail intelligence copilot.

    Your role:
    - help fashion executives
    - analyze inventory risks
    - identify revenue opportunities
    - explain trend acceleration
    - provide strategic recommendations

    USER QUESTION:
    {user_query}

    ===================================
    BUSINESS METRICS
    ===================================

    Revenue Opportunity:
    {business_metrics['revenue_opportunity']}

    Inventory Risk:
    {business_metrics['inventory_risk']}

    Average Confidence:
    {business_metrics['average_confidence']}

    ===================================
    INVENTORY STATE
    ===================================

    {inventory_context}

    ===================================
    HISTORICAL TREND MEMORY
    ===================================

    {historical_trends}

    ===================================
    RETRIEVED RETAIL INTELLIGENCE
    ===================================

    {retrieved_context}

    ===================================
    INSTRUCTIONS
    ===================================

    Generate:
    - executive-level response
    - concise business reasoning
    - inventory intelligence
    - merchandising recommendations
    - risk analysis

    Avoid:
    - generic chatbot responses
    - vague answers
    - unnecessary verbosity

    """

    # -----------------------------------
    # GENERATE RESPONSE
    # -----------------------------------

    response = groq_llm.invoke(
        prompt
    )

    return response.content