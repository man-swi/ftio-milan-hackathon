from crewai import Agent
# from agents.base import groq_llm
from backend.agents.base import groq_llm

inventory_agent = Agent(
    role="Retail Inventory Optimization Specialist",

    goal="""
    Compare current inventory against fashion trends
    and identify understocked and overstocked products.
    Estimate business impact and revenue opportunities.
    """,

    backstory="""
    You are a retail operations expert focused on
    inventory efficiency, stock movement, and
    revenue optimization for fashion brands.
    """,

    llm=groq_llm,

    verbose=False
)