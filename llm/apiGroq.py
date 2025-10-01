from groq import Groq
from dotenv import load_dotenv
import os
import json
from docling.document_converter import DocumentConverter, PdfFormatOption
from docling.datamodel.pipeline_options import (PdfPipelineOptions)
from docling.datamodel.base_models import InputFormat

load_dotenv()
groqKey = os.getenv('GROQ_KEY')
groqClient = Groq(api_key=groqKey)

with open("persona.txt", 'r', encoding='utf-8') as file:
    behavioral = file.read()

with open("identify.txt", 'r', encoding='utf-8') as file:
    identify = file.read()

def processResponse(response):
    answer = ''
    for line in response.text.splitlines():
        if line.strip():  # ignora linhas em branco
            data = json.loads(line)
            if "response" in data:
                answer += data["response"]
    return answer

def getQuestions():
    pipeline_options = PdfPipelineOptions()
    pipeline_options.do_formula_enrichment = True

    doc_converter = DocumentConverter(
    format_options={
        InputFormat.PDF: PdfFormatOption(pipeline_options=pipeline_options)
    })
    result = doc_converter.convert('quests.pdf')
    return result.document.export_to_text()


def setPrompt(quest):
    questions = getQuestions()
    prompt = [
                {
                    "role": "system",
                    "content": identify + "\nlista de perguntas: \n" + questions + "\n\nResposta de uma das perguntas acima: \n" + quest
                }
        ]
    print("PROMPT IDENTIFICAÇÃO:\n\n")
    print(prompt)
    try:
            completion = groqClient.chat.completions.create(
                messages=prompt,
                model="llama-3.3-70b-versatile",
                max_completion_tokens=1024,
                temperature=0.2
            )
            problem = completion.choices[0].message.content

    except Exception:
            return "0) Erro ao acessar api"
    
    print("\n\n\nPROBLEMA IDENTIFICADO\n\n")
    print(problem)

    id = ''
    for ch in problem:
        if ch.isdigit():
            id += ch
        else:
            break
    solution = "solutions/" + id + ".txt"
    with open(solution, 'r', encoding='utf-8') as file:
        solution = file.read()
    print(solution + "\n\n")

    prompt = [
                {
                    "role": "system",
                    "content": behavioral + "\nEnunciado: " + problem + "\nResposta correta da questão: " + solution
                },
                {
                     "role": "user",
                     "content": "\nResposta do aluno que precisa ser corrigida: " + quest
                }
    ]
    return prompt


def getAnswer(quest):
    prompt = setPrompt(quest)
    print("\n\n================================================\n\n" + prompt[1]['content'] + "\n\n===========================================\n\n")
    try:
            completion = groqClient.chat.completions.create(
                messages= prompt,
                model="llama-3.3-70b-versatile",
                max_completion_tokens=1024,
                temperature=0.5
            )
            response = completion.choices[0].message.content

    except Exception:
            return "Erro ao acessar api"

    return response


if __name__ == "__main__":
    question = r"""\documentclass{article}
\usepackage{amsmath}
\begin{document}

\[
u = \ln(x) \quad \Rightarrow \quad du = \frac{1}{x}\,dx,
\qquad
dv = x^2 dx \quad \Rightarrow \quad v = \frac{x^3}{3}.
\]
\[
\int x^2 \ln(x)\,dx
= \frac{x^3}{3}\ln(x) - \int \frac{x^3}{3}\cdot \frac{1}{x}\,dx
= \frac{x^3}{3}\ln(x) - \frac{1}{3}\int x^2\,dx.
\]
\[
\int x^2\,dx = \frac{x^2}{2}.
\]

Substituindo:
\[
\int x^2 \ln(x)\,dx
= \frac{x^3}{3}\ln(x) - \frac{1}{3}\cdot\frac{x^2}{2} + C
= \frac{x^3}{3}\ln(x) - \frac{x^2}{6} + C.
\]

\end{document}"""

    #input("Pergunta: ")
    answer = getAnswer(question)
    print(answer + "\n\n\n")