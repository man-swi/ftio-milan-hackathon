from crewai import Agent
# from agents.base import groq_llm
from backend.agents.base import groq_llm

report_agent = Agent(
    role="Executive Fashion Intelligence Reporter",

    goal="""
    Generate a professional executive report
    summarizing trends, inventory risks,
    opportunities, and recommended actions.
    """,

    backstory="""
    You are a senior retail strategy consultant
    creating concise and actionable business reports
    for fashion executives.
    """,

    llm=groq_llm,

    verbose=False,
    max_iter=1,
    memory=False
)