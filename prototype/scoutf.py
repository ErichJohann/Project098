from groq import Groq
import os
from dotenv import load_dotenv

load_dotenv()
GroqKey = os.getenv('GROQ_KEY')
client = Groq(api_key=GroqKey)

def do_ocr(img_data):

    prompt = [
    {
        "role": "system",
        "content": "Você é um OCR inteligente. Extraia apenas o texto visível da imagem. Se houver cálculos matemáticos, retorne o resultado em LaTeX. Sua resposta deve conter APENAS o texto extraido e nada mais. NÃO ADICIONE EXPLICAÇÔES OU RESULTADOS A MAIS!"
    },
    {
        "role": "user",
        "content": [
            {"type": "text", "text": "Aqui está a imagem:"},
            {"type": "image_url", "image_url": {"url": img_data}}
        ]
    }
]

    completion = client.chat.completions.create(
        model="meta-llama/llama-4-scout-17b-16e-instruct",
        messages=prompt,
        temperature=0.1
    )

    return completion.choices[0].message.content