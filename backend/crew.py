from crewai import Crew, Task

from agents.trend_agent import trend_agent
from agents.inventory_agent import inventory_agent
from agents.report_agent import report_agent

from tools.load_trends import load_mock_trends
from tools.load_inventory import load_inventory

# Load datasets
trend_data = load_mock_trends()
inventory_data = load_inventory().to_dict(orient="records")

# -----------------------------
# TASK 1 — Trend Analysis
# -----------------------------

trend_task = Task(
    description=f"""
    Analyze these fashion trends:

    {trend_data}

    Identify:
    - top trending aesthetics
    - momentum insights
    - strongest categories
    - emerging opportunities
    """,

    expected_output="""
    Structured fashion trend analysis with
    trend rankings, momentum scores,
    and category insights.
    """,

    agent=trend_agent
)

# -----------------------------
# TASK 2 — Inventory Matching
# -----------------------------

inventory_task = Task(
    description=f"""
    Compare these inventory records:

    {inventory_data}

    Against these trends:

    {trend_data}

    Identify:
    - understocked trending products
    - overstocked weak products
    - estimated revenue opportunities
    - inventory risks
    """,

    expected_output="""
    Inventory optimization report with
    stock insights and financial impact.
    """,

    agent=inventory_agent
)

# -----------------------------
# TASK 3 — Executive Report
# -----------------------------

report_task = Task(
    description="""
    Generate a final executive report
    combining trend analysis and inventory insights.

    Include:
    - executive summary
    - top opportunities
    - inventory risks
    - action recommendations
    """,

    expected_output="""
    Professional markdown business report.
    """,

    agent=report_agent
)

# -----------------------------
# CREW
# -----------------------------

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

result = crew.kickoff()

print("\nFINAL REPORT:\n")
print(result)