from groq import Groq
from dotenv import load_dotenv
import os
import json
from docling.document_converter import DocumentConverter, PdfFormatOption
from docling.datamodel.pipeline_options import (PdfPipelineOptions)
from docling.datamodel.base_models import InputFormat

load_dotenv()
GroqKey = os.getenv('GROQ_KEY')
client = Groq(api_key=GroqKey)

with open("identify.txt", 'r', encoding='utf-8') as file:
    identify = file.read()

with open("persona.txt", 'r', encoding='utf-8') as file:
    behavioral = file.read()


def getQuestions():
    pipeline_options = PdfPipelineOptions()
    pipeline_options.do_formula_enrichment = True

    doc_converter = DocumentConverter(
    format_options={
        InputFormat.PDF: PdfFormatOption(pipeline_options=pipeline_options)
    })
    result = doc_converter.convert('quests.pdf')
    return result.document.export_to_text()


def getAnswer(problem):
    num = ''
    for ch in problem:
        if ch.isdigit():
            num += ch
        else:
            break
    solution = "solutions/" + num + ".txt"

    with open(solution, 'r', encoding='utf-8') as file:
        solution = file.read()

    return solution


def setPrompt(quest):
    questions = getQuestions()
    prompt = [
                {
                    "role": "system",
                    "content": identify + "\nlista de perguntas: \n" + questions + "\n\nResposta de uma das perguntas acima: \n" + quest
                }
        ]

    try:
            completion = client.chat.completions.create(
                messages=prompt,
                model="llama-3.3-70b-versatile",
                max_completion_tokens=1024,
                temperature=0.2
            )
            problem = completion.choices[0].message.content

    except Exception:
            print("Erro ao acessar api")
            exit(2)

    solution = getAnswer(problem)

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