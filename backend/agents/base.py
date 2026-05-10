from crewai import LLM
import os
from dotenv import load_dotenv

load_dotenv()

groq_llm = LLM(
    model="groq/llama3-8b-8192",
    api_key=os.getenv("GROQ_API_KEY")
)