import os
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM, GenerationConfig, pipeline
from groq import Groq
from dotenv import load_dotenv

load_dotenv()
groqKey = os.getenv('GROQ_KEY')

os.environ["HF_HUB_DISABLE_SYMLINKS_WARNING"] = 'True'
device = 'cuda' if torch.cuda.is_available() else 'cpu'
print("Usando:", device)

question = r"$\int x ^ { 2 } \ln ( x ) \, d x$"
student = r"""$\int x^2 \ln(x) dx$
    $v = x^2   du = \ln(x) dx$
    $dv = 2x dx    u = x\ln(x) - x$
    $= x^2.(x \ln(x) -x) - \int (x \ln(x) -x)2x dx$"""
solution_reasoning = r"""$$\int x^2\ln(x)\,dx$$Usamos a integração por partes, onde escolhemos:$u=\ln(x)$, o que implica $du=\frac{1}{x}dx$$dv=x^2dx$, o que implica $v=\frac{x^3}{3}$Aplicando a fórmula da integração por partes ($\int u\,dv = uv - \int v\,du$):$$\int x^2\ln(x)\,dx
= \frac{x^3}{3}\ln(x) - \int \frac{x^3}{3}\cdot\frac{1}{x}\,dx$$Simplificando a nova integral:$$\frac{x^3}{3}\ln(x) - \int \frac{x^2}{3}\,dx
= \frac{x^3}{3}\ln(x) - \frac{1}{3}\int x^2\,dx$$Finalmente, integrando $\int x^2\,dx$:$$\int x^2\ln(x)\,dx
= \frac{x^3}{3}\ln(x) - \frac{1}{3}\cdot\frac{x^3}{3} + C$$O resultado final é:$$\frac{x^3}{3}\ln(x) - \frac{x^3}{9} + C$$"""
solution_raw = r"""$\int x^2\ln(x)\,dx$ $\int x^2\ln(x)\,dx
= \frac{x^3}{3}\ln(x) - \int \frac{x^3}{3}\cdot\frac{1}{x}\,dx$ $= \frac{x^3}{3}\ln(x) - \frac{1}{3}\int x^2\,dx$ $= \frac{x^3}{3}\ln(x) - \frac{1}{3}\cdot\frac{x^3}{3} + C$ $= \frac{x^3}{3}\ln(x) - \frac{x^3}{9} + C$"""

def deepseek():
    model_name = "deepseek-ai/deepseek-math-7b-instruct"
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForCausalLM.from_pretrained(model_name,
                                                 device_map={ "": device },   # Força tudo no device correto
                                                 torch_dtype="auto")           # deixa o Transformers otimizar, offload_folder="offload")
    model.generation_config = GenerationConfig.from_pretrained(model_name)
    model.generation_config.pad_token_id = model.generation_config.eos_token_id

    messages = [
        {"role": "user", 
         "content": "Questão: " + question + "\nSolução: " + solution_raw + "\nResposta do aluno: " + student +
         "\nInstrução: Por favor atue como um professor indicando onde a resposta do aluno diverge da solução e como corrigir, coloque sua resposta final em \\boxed{}."}
    ]
    input_tensor = tokenizer.apply_chat_template(messages, add_generation_prompt=True, return_tensors="pt")
    outputs = model.generate(input_tensor.to(model.device), max_new_tokens=1024)

    result = tokenizer.decode(outputs[0][input_tensor.shape[1]:], skip_special_tokens=True)
    return result

def qwen():
    model_name = "Qwen/Qwen2-Math-7B-Instruct"
    model = AutoModelForCausalLM.from_pretrained(
    model_name,
    torch_dtype="auto",
    #load_in_4bit=True, only works on gpu?
    device_map=device
    )
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    prompt = "Find any mistake on the student's answer" + "\nProblem: " + question + "\nRight solution:" + solution_raw +  "\n\nStudent's try: " + student
    messages = [
        {"role": "system", "content": "You are a teacher, you must indicate where the solution of the student goes wrong and how to proceed"},
        {"role": "user", "content": prompt}
    ]
    text = tokenizer.apply_chat_template(
    messages,
    tokenize=False,
    add_generation_prompt=True
    )
    model_inputs = tokenizer([text], return_tensors="pt").to(device)
    generated_ids = model.generate(
    **model_inputs,
    max_new_tokens=512,
    do_sample=False
    )
    generated_ids = [
    output_ids[len(input_ids):] for input_ids, output_ids in zip(model_inputs.input_ids, generated_ids)
    ]
    response = tokenizer.batch_decode(generated_ids, skip_special_tokens=True)[0]

    return response

def mathstral():
    checkpoint = "mistralai/Mathstral-7b-v0.1"
    pipe = pipeline("text-generation", checkpoint, device_map="auto", torch_dtype='auto')

    prompt = [{"role": "user", "content": "Find any mistake on the student's answer" + "\nProblem: " + question + "\nRight solution:" + solution_raw +  "\n\nStudent's try: " + student}]
    out = pipe(prompt, max_new_tokens = 512)

    response = out[0]['generated_text']

    return response

def gemma():
    tokenizer = AutoTokenizer.from_pretrained("google/gemma-2-9b-it")
    model = AutoModelForCausalLM.from_pretrained(
        "google/gemma-2-9b-it",
        device_map=device,
        torch_dtype="auto",
    )
    prompt = [{"role": "user", "content": "Find any mistake on the student's answer" + "\nProblem: " + question + "\nRight solution:" + solution_raw +  "\n\nStudent's try: " + student}]
    input_ids = tokenizer.apply_chat_template(prompt, return_tensors="pt", return_dict=True)
    if device == "cuda":
        input_ids = input_ids.to("cuda")

    outputs = model.generate(**input_ids, max_new_tokens=512)
    response = tokenizer.decode(outputs[0], skip_special_tokens=True)
    
def phi():
    #torch.random.manual_seed(0) 
    model = AutoModelForCausalLM.from_pretrained( 
        "microsoft/Phi-3-mini-128k-instruct",  
        device_map="auto",  
        torch_dtype="auto",  
        trust_remote_code=True,  
    ) 

    tokenizer = AutoTokenizer.from_pretrained("microsoft/Phi-3-mini-128k-instruct") 

    messages = [
        {"role": "system", "content": "You are a math teacher. You must evaluate the student's answer."},
        {"role": "user", "content": f"Problem:\n{question}\n\nCorrect solution:\n{solution_raw}\n\nStudent's attempt:\n{student}\n\nIdentify the mistake and explain."}
    ]

    prompt = tokenizer.apply_chat_template(
        messages,
        tokenize=False,
        add_generation_prompt=True
    )
    pipe = pipeline( 
        "text-generation", 
        model=model, 
        tokenizer=tokenizer, 
    ) 

    generation_args = { 
        "max_new_tokens": 500, 
        "return_full_text": False, 
        "temperature": 0.1, 
        "do_sample": False, 
    } 

    output = pipe(prompt, **generation_args) 
    response = output[0]['generated_text']
    return response


def gpt():
    client = Groq(api_key=groqKey)
    prompt = [
        {"role": "system", "content": "You are a math teacher. You must evaluate the student's answer."},
        {"role": "user", "content": f"Problem:\n{question}\n\nCorrect solution:\n{solution_raw}\n\nStudent's attempt:\n{student}\n\nIdentify the mistake and explain."}
    ]

    completion = client.chat.completions.create(
        model="openai/gpt-oss-120b",
        messages=prompt,
        temperature=0.5,
        max_completion_tokens=1024,
        top_p=1,
        reasoning_effort="medium",
        stream=True,
        stop=None
    )

    for chunk in completion:
        print(chunk.choices[0].delta.content or "", end="")

    return ''

def groqQwen():
    client = Groq(api_key=groqKey)
    prompt = [
        {"role": "system", "content": "You are a math teacher. You must evaluate the student's answer."},
        {"role": "user", "content": f"Problem:\n{question}\n\nCorrect solution:\n{solution_raw}\n\nStudent's attempt:\n{student}\n\nIdentify the mistake and explain."}
    ]

    completion = client.chat.completions.create(
        model="qwen/qwen3-32b",
        messages=prompt,
        temperature=0.3,
        max_completion_tokens=1024,
        top_p=0.95,
        reasoning_effort="default",
        stream=True,
        stop=None
    )

    for chunk in completion:
        print(chunk.choices[0].delta.content or "", end="")

    return ""

def gpt_smaller():
    client = Groq(api_key=groqKey)
    prompt = [
        {"role": "system", "content": "You are a math teacher. You must evaluate the student's answer."},
        {"role": "user", "content": f"Problem:\n{question}\n\nCorrect solution:\n{solution_raw}\n\nStudent's attempt:\n{student}\n\nIdentify the mistake and explain."}
    ]

    completion = client.chat.completions.create(
        model="openai/gpt-oss-20b",
        messages=prompt,
        temperature=0.5,
        max_completion_tokens=1024,
        top_p=1,
        reasoning_effort="medium",
        stream=True,
        stop=None
    )

    for chunk in completion:
        print(chunk.choices[0].delta.content or "", end="")

    return ''

#answer = deepseek()
#answer = qwen()
#answer = mathstral()
#answer = phi()
answer = gemma()
#answer = gpt()
#answer = groqQwen()
#answer = gpt_smaller()
print(answer)