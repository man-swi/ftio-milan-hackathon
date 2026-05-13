from crewai import LLM
from groq import Groq

import os
from dotenv import load_dotenv

load_dotenv()

# -----------------------------------
# CREWAI LLM
# -----------------------------------

groq_llm = LLM(
    model="groq/llama-3.3-70b-versatile",
    api_key=os.getenv("GROQ_API_KEY"),
    temperature=0.3,
    max_tokens=350
)

# -----------------------------------
# DIRECT GROQ CLIENT
# -----------------------------------

groq_client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

# -----------------------------------
# DIRECT GROQ RESPONSE
# -----------------------------------

def generate_groq_response(
    prompt
):

    completion = groq_client.chat.completions.create(

        model="llama-3.3-70b-versatile",

        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],

        temperature=0.4,
        max_tokens=350
    )

    return completion.choices[0].message.content