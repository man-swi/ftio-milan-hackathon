from crewai import Agent

from backend.agents.base import groq_llm


reflection_agent = Agent(

    role="Retail Risk Intelligence Analyst",

    goal="""
    Critically evaluate:
    - inventory decisions
    - merchandising strategies
    - forecasting assumptions
    - operational risks

    Use:
    - retrieved retail intelligence
    - fashion cycle behavior
    - inventory risk heuristics
    """,

    backstory="""
    You specialize in:
    - inventory volatility
    - fashion trend instability
    - overstock exposure
    - merchandising failures
    - retail operational risk

    Your critiques should:
    - identify weak assumptions
    - explain operational exposure
    - reference historical fashion behavior
    - avoid generic warnings
    """,

    llm=groq_llm,

    verbose=False,

    max_iter=1,

    memory=False
)