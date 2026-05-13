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
# RUN FTIO ANALYSIS
# -----------------------------------

def run_ftio_analysis():

    # -----------------------------------
    # RETRIEVE KNOWLEDGE
    # -----------------------------------

    retrieved_knowledge = retrieve_context(
        "fashion inventory optimization, trend forecasting, merchandising strategy",
        top_k=1
    )

    # -----------------------------------
    # LOAD DATA
    # -----------------------------------

    trend_data = load_mock_trends()

    inventory_df = load_inventory()

    if isinstance(inventory_df, list):

        inventory_data = inventory_df

    else:

        inventory_data = inventory_df.to_dict(
            orient="records"
        )

    # -----------------------------------
    # BUSINESS METRICS
    # -----------------------------------

    business_metrics = (
        calculate_business_metrics(
            trend_data,
            inventory_data
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

            "trend":
            trend["trend"],

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
            ],

            "volatility_score":
            temporal_result[
                "volatility_score"
            ]
        })

    # ===================================
    # TREND ANALYSIS TASK
    # ===================================

    trend_task = Task(

        description=f"""
        Analyze fashion trend momentum,
        acceleration,
        demand evolution,
        and category growth.

        Trend Data:
        {trend_data}

        Temporal Insights:
        {temporal_insights}

        IMPORTANT:

        - identify strongest trends
        - identify accelerating trends
        - identify weakening trends
        - rank trends by business value
        - use concise executive language
        """,

        expected_output="""
        Return executive trend intelligence.

        Include:
        - strongest trend
        - fastest accelerating trend
        - weakening trend
        - highest opportunity category

        Maximum 4 bullets.
        Maximum 60 words.
        """,

        agent=trend_agent
    )

    # ===================================
    # INVENTORY ANALYSIS TASK
    # ===================================

    inventory_task = Task(

        description=f"""
        Analyze inventory exposure,
        stock imbalance,
        demand alignment,
        and operational risk.

        Inventory Data:
        {inventory_data}

        IMPORTANT:

        - identify understock risk
        - identify overstock risk
        - identify inventory bottlenecks
        - identify high-margin opportunities
        - prioritize highest-risk products
        """,

        expected_output="""
        Return executive inventory intelligence.

        Include:
        - highest inventory risk
        - highest stockout risk
        - highest revenue opportunity
        - weakest inventory position

        Maximum 4 bullets.
        Maximum 60 words.
        """,

        context=[trend_task],

        agent=inventory_agent
    )

    # ===================================
    # STRATEGY TASK
    # ===================================

    strategy_task = Task(

        description=f"""
        Generate executive retail strategy.

        Retail Intelligence:
        {retrieved_knowledge}

        Temporal Intelligence:
        {temporal_insights}

        IMPORTANT:

        Build strategic actions using:
        - trend acceleration
        - inventory positioning
        - category demand
        - seasonal behavior
        - historical fashion cycles

        IMPORTANT:
        - prioritize revenue efficiency
        - prioritize inventory optimization
        - prioritize trend scalability
        - avoid generic recommendations
        """,

        expected_output="""
        Return strategic recommendations.

        Include:
        - top merchandising action
        - category prioritization
        - inventory allocation strategy
        - seasonal optimization

        Maximum 4 bullets.
        Maximum 80 words.
        """,

        context=[
            trend_task,
            inventory_task
        ],

        agent=strategy_agent
    )

    # ===================================
    # REFLECTION TASK
    # ===================================

    reflection_task = Task(

        description=f"""
        Critically challenge the proposed
        retail strategies and identify risks.

        Retail Intelligence:
        {retrieved_knowledge}

        IMPORTANT:

        Focus on:
        - trend instability
        - false momentum
        - inventory saturation
        - operational weakness
        - merchandising inefficiencies
        - economic uncertainty

        IMPORTANT:
        - disagree where necessary
        - challenge assumptions
        - identify weak logic
        - identify overconfidence risk
        - identify hidden operational risk
        """,

        expected_output="""
        Return executive risk reflection.

        Include:
        - weakest recommendation
        - hidden operational risk
        - overstock vulnerability
        - unstable trend signal

        Maximum 4 bullets.
        Maximum 60 words.
        """,

        context=[
            trend_task,
            inventory_task,
            strategy_task
        ],

        agent=reflection_agent
    )

    # ===================================
    # CONSENSUS SYNTHESIS TASK
    # ===================================

    consensus_task = Task(

        description=f"""
        Synthesize all agent outputs into
        one final executive decision framework.

        IMPORTANT:

        Perform:
        - agent disagreement resolution
        - strategic prioritization
        - risk-weighted consensus
        - executive scoring
        - final action ranking

        IMPORTANT:

        Reflection agent objections MUST override
        weak strategic recommendations if risk
        exposure is too high.

        IMPORTANT:
        - avoid repetition
        - avoid generic summaries
        - think like a retail executive board
        """,

        expected_output="""
        Return final executive consensus.

        REQUIRED FORMAT:

        1. Highest Priority Decision
        2. Highest Risk Warning
        3. Best Revenue Opportunity
        4. Most Unstable Trend
        5. Final Strategic Recommendation

        Maximum 100 words.
        """,

        context=[
            trend_task,
            inventory_task,
            strategy_task,
            reflection_task
        ],

        agent=strategy_agent
    )

    # ===================================
    # CREW
    # ===================================

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

            reflection_task,

            consensus_task
        ],

        verbose=False,

        max_rpm=8
    )

    # ===================================
    # EXECUTE CREW
    # ===================================

    result = crew.kickoff()

    # ===================================
    # OUTPUTS
    # ===================================

    trend_output = str(
        trend_task.output
    )

    inventory_output = str(
        inventory_task.output
    )

    strategy_output = str(
        strategy_task.output
    )

    reflection_output = str(
        reflection_task.output
    )

    consensus_output = str(
        consensus_task.output
    )

    metrics = business_metrics

    # ===================================
    # SAVE MEMORY
    # ===================================

    persist_analysis_memory(

        trend_data,

        metrics,

        strategy_output,

        reflection_output
    )

    # ===================================
    # FINAL REPORT
    # ===================================

    final_report = f"""

# FTIO Executive Intelligence Report

---

# Executive Summary

FTIO executed a collaborative
multi-agent retail intelligence cycle.

---

# Business Metrics

- Revenue Opportunity:
${metrics['total_revenue_opportunity']}

- Inventory Risk:
${metrics['total_inventory_risk']}

- Average Confidence:
{metrics['average_confidence']}

---

# Temporal Intelligence

"""

    # ===================================
    # TEMPORAL REPORTING
    # ===================================

    for insight in temporal_insights:

        final_report += f"""

## {insight['trend']}

- Previous Momentum:
{insight['previous_momentum']}

- Current Momentum:
{insight['current_momentum']}

- Momentum Change:
{insight['momentum_change']}%

- Trend Status:
{insight['acceleration_label']}

- Volatility Score:
{insight['volatility_score']}
"""

    # ===================================
    # AGENT OUTPUTS
    # ===================================

    final_report += f"""

---

# Trend Intelligence

{trend_output}

---

# Inventory Intelligence

{inventory_output}

---

# Strategic Recommendations

{strategy_output}

---

# Risk Reflection

{reflection_output}

---

# Executive Consensus

{consensus_output}

---
"""

    # ===================================
    # SAVE REPORT
    # ===================================

    with open(

        "backend/reports/final_report.md",

        "w",

        encoding="utf-8"

    ) as file:

        file.write(final_report)

    # ===================================
    # RETURN RESPONSE
    # ===================================

    return {

        "status": "success",

        "report": final_report,

        "metrics": metrics,

        "temporal_insights":
        temporal_insights,

        "trend_output":
        trend_output,

        "inventory_output":
        inventory_output,

        "strategy_output":
        strategy_output,

        "reflection_output":
        reflection_output,

        "consensus_output":
        consensus_output
    }