from groq import Groq
from dotenv import load_dotenv
import os
import base64
import tkinter as tk
from tkinter import filedialog

load_dotenv()
GroqKey = os.getenv('GROQ_KEY')
client = Groq(api_key=GroqKey)

# Cria a janela principal oculta (não precisa mostrar nada)
root = tk.Tk()
root.withdraw()  # esconde a janela principal

# Abre o seletor de arquivos
file_path = filedialog.askopenfilename(
    title="Selecione uma imagem",
    filetypes=[("Imagens", "*.png *.jpg *.jpeg")]
)

if file_path:
    # Converte o arquivo escolhido em base64
    with open(file_path, "rb") as f:
        img_base64 = base64.b64encode(f.read()).decode("utf-8")

    # Monta a string no formato data:image
    if file_path.lower().endswith(".png"):
        prefix = "data:image/png;base64,"
    elif file_path.lower().endswith((".jpg", ".jpeg")):
        prefix = "data:image/jpeg;base64,"
    else:
        prefix = "data:image/*;base64,"

    img_data = prefix + img_base64
else:
    exit(1)


# Faz a chamada ao modelo multimodal (Llama 4 Scout)
completion = client.chat.completions.create(
        model="meta-llama/llama-4-scout-17b-16e-instruct",
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": "Extraia todo o texto da imagem a seguir. Não adicione NADA, retorne APENAS o texto identificado. Caso se trate de cálculos matemáticos retorne o resultado em LaTeX"},
                    {"type": "image_url", "image_url": {"url": img_data}}
                ]
            }
        ]
    )
print(completion.choices[0].message.content)