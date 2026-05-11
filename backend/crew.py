from backend.agents.trend_agent import trend_agent
from backend.agents.inventory_agent import inventory_agent
from backend.agents.report_agent import report_agent

from backend.tools.load_trends import load_mock_trends
from backend.tools.load_inventory import load_inventory
from crewai import Crew, Task

# -----------------------------------
# LOAD DATASETS
# -----------------------------------

trend_data = load_mock_trends()

inventory_data = load_inventory().to_dict(
    orient="records"
)

# -----------------------------------
# TASK 1 — TREND ANALYSIS
# -----------------------------------

trend_task = Task(
    description=f"""
    Analyze the following fashion trend dataset:

    {trend_data}

    Your responsibilities:
    - identify top trending aesthetics
    - analyze momentum scores
    - identify strongest fashion categories
    - identify emerging opportunities
    - summarize consumer behavior patterns

    Focus on actionable business intelligence.
    """,

    expected_output="""
    A structured fashion trend analysis report including:
    - trend rankings
    - strongest categories
    - momentum insights
    - emerging opportunities
    - consumer behavior observations
    """,

    agent=trend_agent
)

# -----------------------------------
# TASK 2 — INVENTORY ANALYSIS
# -----------------------------------

inventory_task = Task(
    description=f"""
    Analyze the inventory dataset below:

    {inventory_data}

    Compare inventory performance against
    the previously analyzed fashion trends.

    Your responsibilities:
    - identify understocked trending products
    - identify overstocked weak products
    - estimate revenue opportunities
    - estimate inventory risks
    - recommend inventory adjustments

    Focus on retail optimization and financial impact.
    """,

    expected_output="""
    A structured inventory optimization report including:
    - understock risks
    - overstock risks
    - financial opportunities
    - inventory recommendations
    - estimated business impact
    """,

    context=[trend_task],

    agent=inventory_agent
)

# -----------------------------------
# TASK 3 — EXECUTIVE REPORT
# -----------------------------------

report_task = Task(
    description="""
    Generate a final executive-level fashion
    intelligence report.

    Combine:
    - trend analysis
    - inventory optimization insights
    - financial opportunities
    - inventory risks
    - business recommendations

    The report should be concise,
    professional, and business-focused.

    Use markdown formatting.
    """,

    expected_output="""
    A professional executive markdown report containing:
    - executive summary
    - top opportunities
    - inventory risks
    - recommended actions
    - financial insights
    - trend intelligence summary
    """,

    context=[
        trend_task,
        inventory_task
    ],

    agent=report_agent
)

# -----------------------------------
# CREW ORCHESTRATION
# -----------------------------------

crew = Crew(
    agents=[
        trend_agent,
        inventory_agent,
        report_agent
    ],

    tasks=[
        trend_task,
        inventory_task,
        report_task
    ],

    verbose=True
)

# -----------------------------------
# RUN ANALYSIS FUNCTION
# -----------------------------------

def run_ftio_analysis():

    result = crew.kickoff()

    with open(
        "backend/reports/final_report.md",
        "w",
        encoding="utf-8"
    ) as file:

        file.write(str(result))

    return str(result)