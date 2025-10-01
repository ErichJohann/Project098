import requests
import json
from docling.document_converter import DocumentConverter, PdfFormatOption
from docling.datamodel.pipeline_options import (PdfPipelineOptions)
from docling.datamodel.base_models import InputFormat

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
    prompt = identify + "\nlista de perguntas: \n" + questions + "\n\nResposta de uma das perguntas acima: \n" + quest
    print(prompt + '\n\n\n')
    response = requests.post(
        "http://localhost:11434/api/generate",
        json={"model": "llama3.1", "prompt": prompt, "temperature": 0.2},
        stream=False
    )
    problem = processResponse(response)
    print(problem + "\n\n")

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

    prompt = behavioral + "\nEnunciado: " + problem + "\nResposta correta da questão: " + solution +"\nResposta do aluno que precisa ser corrigida: " + quest
    return prompt


def getAnswer(quest):
    prompt = setPrompt(quest)
    print("\n\n================================================\n" + prompt + "\n===========================================\n\n")
    response = requests.post(
        "http://localhost:11434/api/generate",
        json={"model": "llama3.1", "prompt": prompt, "temperature": 0.5},
        stream=False
    )
    correction = processResponse(response)
    return correction


if __name__ == "__main__":
    question = "a arquitetura de von newmann é uma cpu e uma memória ram"
    #input("Pergunta: ")
    answer = getAnswer(question)
    print(answer + "\n\n\n")