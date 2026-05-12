from crewai import Crew, Task

from backend.services.business_metrics import (
    calculate_business_metrics
)

from backend.agents.trend_agent import (
    trend_agent
)

from backend.agents.inventory_agent import (
    inventory_agent
)

from backend.agents.report_agent import (
    report_agent
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
# TREND TASK
# -----------------------------------

trend_task = Task(

    description=f"""
    Analyze the following fashion trend dataset:

    {trend_data}

    Focus on:
    - momentum acceleration
    - trend confidence
    - consumer behavior shifts
    - high-growth categories
    - seasonal demand signals

    Generate enterprise-grade trend intelligence.
    """,

    expected_output="""
    Detailed trend intelligence report including:
    - trend rankings
    - category analysis
    - acceleration insights
    - demand forecasting
    - consumer behavior patterns
    """,

    agent=trend_agent
)

# -----------------------------------
# INVENTORY TASK
# -----------------------------------

inventory_task = Task(

    description=f"""
    Analyze the inventory dataset below:

    {inventory_data}

    Compare inventory performance against
    trend momentum and confidence levels.

    Focus on:
    - understock risks
    - overstock exposure
    - inventory imbalance
    - revenue opportunities
    - operational inefficiencies
    """,

    expected_output="""
    Enterprise inventory optimization report
    with financial and operational insights.
    """,

    context=[trend_task],

    agent=inventory_agent
)

# -----------------------------------
# STRATEGY TASK
# -----------------------------------

strategy_task = Task(

    description="""
    Generate advanced retail growth strategies.

    Focus on:
    - merchandising optimization
    - bundling opportunities
    - campaign strategies
    - pricing recommendations
    - inventory reallocation
    - category prioritization

    Use simulation insights and
    business forecasting logic.
    """,

    expected_output="""
    Strategic retail action plan including:
    - campaign ideas
    - merchandising strategy
    - pricing strategy
    - inventory allocation strategy
    - expected business impact
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

    description="""
    Critically evaluate all previous
    recommendations and identify:

    - uncertainty
    - forecasting risks
    - low-confidence trends
    - operational weaknesses
    - unstable assumptions

    Challenge weak recommendations.
    """,

    expected_output="""
    Risk analysis and reflection report
    highlighting uncertainty, volatility,
    and recommendation risks.
    """,

    context=[
        trend_task,
        inventory_task,
        strategy_task
    ],

    agent=reflection_agent
)

# -----------------------------------
# REPORT TASK
# -----------------------------------

report_task = Task(

    description="""
    Generate a final executive-level
    retail decision intelligence report.

    Combine:
    - trend intelligence
    - inventory optimization
    - forecasting simulations
    - strategic recommendations
    - reflection warnings
    - financial opportunities
    - operational risks

    Use professional markdown formatting.
    """,

    expected_output="""
    Executive retail intelligence report containing:
    - executive summary
    - trend intelligence
    - inventory analysis
    - business simulations
    - strategic recommendations
    - risk analysis
    - reflection insights
    - financial forecasts
    """,

    context=[
        trend_task,
        inventory_task,
        strategy_task,
        reflection_task
    ],

    agent=report_agent
)

# -----------------------------------
# CREW
# -----------------------------------

crew = Crew(

    agents=[
        trend_agent,
        inventory_agent,
        strategy_agent,
        reflection_agent,
        report_agent
    ],

    tasks=[
        trend_task,
        inventory_task,
        strategy_task,
        reflection_task,
        report_task
    ],

    verbose=True
)

# -----------------------------------
# RUN FUNCTION
# -----------------------------------

def run_ftio_analysis():

    result = crew.kickoff()

    final_report = str(result)

    with open(
        "backend/reports/final_report.md",
        "w",
        encoding="utf-8"
    ) as file:

        file.write(final_report)

    return {

        "status": "success",

        "report": final_report,

        "metrics": business_metrics
    }