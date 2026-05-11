from crewai import Agent
# from agents.base import groq_llm
from backend.agents.base import groq_llm

trend_agent = Agent(
    role="Senior Fashion Trend Analyst",

    goal="""
    Analyze fashion trend data and identify
    emerging trends with momentum scores,
    confidence levels, and category insights.
    """,

    backstory="""
    You are an elite fashion intelligence analyst
    specializing in detecting viral fashion movements,
    aesthetics, and consumer buying patterns.
    """,

    llm=groq_llm,

    verbose=True
)