from groq import Groq
import os
from dotenv import load_dotenv

load_dotenv()
GroqKey = os.getenv('GROQ_KEY')
client = Groq(api_key=GroqKey)

def getAnswer(prompt):
    try:
        completion = client.chat.completions.create(
            messages= prompt,
            model="llama-3.3-70b-versatile",
            max_completion_tokens=1024,
            temperature=0.5
        )

    except Exception:
        return "Erro ao acessar api"
        exit(3)

    return completion.choices[0].message.content
