from crewai import Crew, Task

from backend.services.business_metrics import (
    calculate_business_metrics
)

from backend.services.memory_engine import (
    persist_analysis_memory
)

from backend.services.temporal_analysis import (
    calculate_momentum_acceleration
)

from backend.services.rag_engine import (
    retrieve_context
)

from backend.agents.trend_agent import (
    trend_agent
)

from backend.agents.inventory_agent import (
    inventory_agent
)

from backend.agents.strategy_agent import (
    strategy_agent
)

from backend.agents.reflection_agent import (
    reflection_agent
)

from backend.tools.load_trends import (
    load_mock_trends
)

from backend.tools.load_inventory import (
    load_inventory
)

# -----------------------------------
# RUN FUNCTION
# -----------------------------------

def run_ftio_analysis():

    # -----------------------------------
    # RETRIEVE DOMAIN KNOWLEDGE
    # -----------------------------------

    retrieved_knowledge = retrieve_context(
        "fashion inventory optimization, trend forecasting, merchandising strategy"
    )

    # -----------------------------------
    # LOAD DATA
    # -----------------------------------

    trend_data = load_mock_trends()

    inventory_df = load_inventory()

    inventory_data = inventory_df.to_dict(
        orient="records"
    )

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
    # TEMPORAL INTELLIGENCE
    # -----------------------------------

    temporal_insights = []

    for trend in trend_data:

        temporal_result = (
            calculate_momentum_acceleration(

                trend["trend"],
                trend["momentum"]

            )
        )

        temporal_insights.append({

            "trend": trend["trend"],

            "previous_momentum":
            temporal_result[
                "previous_momentum"
            ],

            "current_momentum":
            temporal_result[
                "current_momentum"
            ],

            "momentum_change":
            temporal_result[
                "momentum_change"
            ],

            "acceleration_label":
            temporal_result[
                "acceleration_label"
            ]
        })

    # -----------------------------------
    # TREND TASK
    # -----------------------------------

    trend_task = Task(

        description=f"""
        Analyze current fashion trend data.

        Focus on:
        - strongest momentum
        - trend acceleration
        - demand shifts
        - category opportunities

        Current trends:
        {trend_data}

        Temporal insights:
        {temporal_insights}
        """,

        expected_output="""
        Return concise trend intelligence.

        Maximum 5 bullets.
        Maximum 120 words.
        """,

        agent=trend_agent
    )

    # -----------------------------------
    # INVENTORY TASK
    # -----------------------------------

    inventory_task = Task(

        description=f"""
        Analyze inventory risks and opportunities.

        Inventory data:
        {inventory_data}
        """,

        expected_output="""
        Return concise inventory insights.

        Maximum 5 bullets.
        Maximum 120 words.
        """,

        context=[trend_task],

        agent=inventory_agent
    )

    # -----------------------------------
    # STRATEGY TASK
    # -----------------------------------

    strategy_task = Task(

        description=f"""
Generate contextual retail strategies.

Retrieved Retail Intelligence:
{retrieved_knowledge}

Focus on:
- merchandising optimization
- inventory allocation
- pricing strategy
- trend acceleration
- seasonal demand behavior

IMPORTANT:
- Use retrieved retail intelligence
- Reference historical fashion behavior
- Avoid generic recommendations
- Explain business reasoning
""",

        expected_output="""
        Return concise retail actions.

        Maximum 5 bullets.
        Maximum 150 words.
        """,

        context=[
            trend_task,
            inventory_task
        ],

        agent=strategy_agent
    )

    # -----------------------------------
    # REFLECTION TASK
    # -----------------------------------

    reflection_task = Task(

        description=f"""
Critically analyze operational risks.

Retrieved Retail Intelligence:
{retrieved_knowledge}

Focus on:
- trend instability
- inventory volatility
- overstock exposure
- merchandising weakness
- seasonal saturation risk

IMPORTANT:
- Use retrieved retail intelligence
- Reference fashion behavior patterns
- Explain risk drivers
- Avoid generic warnings
""",

        expected_output="""
        Return concise risk analysis.

        Maximum 5 bullets.
        Maximum 120 words.
        """,

        context=[
            trend_task,
            inventory_task,
            strategy_task
        ],

        agent=reflection_agent
    )

    # -----------------------------------
    # CREW
    # -----------------------------------

    crew = Crew(

        agents=[
            trend_agent,
            inventory_agent,
            strategy_agent,
            reflection_agent
        ],

        tasks=[
            trend_task,
            inventory_task,
            strategy_task,
            reflection_task
        ],

        verbose=False
    )

    result = crew.kickoff()

    strategy_output = str(
        strategy_task.output
    )

    reflection_output = str(
        reflection_task.output
    )

    metrics = business_metrics

    # -----------------------------------
    # SAVE MEMORY
    # -----------------------------------

    persist_analysis_memory(

        trend_data,
        metrics,
        strategy_output,
        reflection_output
    )

    # -----------------------------------
    # REPORT
    # -----------------------------------

    final_report = f"""
# FTIO Executive Intelligence Report

---

## Executive Summary

FTIO detected evolving fashion trends
using temporal intelligence and
historical momentum tracking.

The system identified acceleration
signals, inventory risks,
and revenue opportunities.

---

## Business Metrics

- Revenue Opportunity:
${metrics['total_revenue_opportunity']}

- Inventory Risk:
${metrics['total_inventory_risk']}

- Average Confidence:
{metrics['average_confidence']}

---

## Temporal Intelligence

"""

    for insight in temporal_insights:

        final_report += f"""
### {insight['trend'].title()}

- Previous Momentum:
{insight['previous_momentum']}

- Current Momentum:
{insight['current_momentum']}

- Momentum Change:
{insight['momentum_change']}%

- Trend Status:
{insight['acceleration_label']}
"""

    final_report += f"""

---

## Strategy Recommendations

{strategy_output}

---

## Risk Reflection

{reflection_output}

---
"""

    with open(
        "backend/reports/final_report.md",
        "w",
        encoding="utf-8"
    ) as file:

        file.write(final_report)

    return {

        "status": "success",

        "report": final_report,

        "metrics": metrics,

        "temporal_insights":
        temporal_insights
    }