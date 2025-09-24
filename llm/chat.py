import requests
import json

with open("persona.txt", 'r', encoding='utf-8') as file:
    behavioral = file.read()

def getAnswer(quest):
    prompt = behavioral + "\nresposta do aluno: " + quest
    response = requests.post(
        "http://localhost:11434/api/generate",
        json={"model": "llama3.1", "prompt": prompt},
        stream=False
    )

    answer = ''
    for line in response.text.splitlines():
        if line.strip():  # ignora linhas em branco
            data = json.loads(line)
            if "response" in data:
                answer += data["response"]

    return answer

if __name__ == "__main__":
    question = input("Pergunta: ")
    answer = getAnswer(question)
    print(answer + "\n\n\n")