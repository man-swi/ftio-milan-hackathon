from groq import Groq
from dotenv import load_dotenv
import os

load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

def test_llm():
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "user",
                "content": "Give 3 emerging fashion trends in 2025."
            }
        ]
    )

    return response.choices[0].message.content

if __name__ == "__main__":
    print(test_llm())