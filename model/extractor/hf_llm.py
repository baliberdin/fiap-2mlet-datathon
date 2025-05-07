from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline
import torch

# Use um modelo mais leve e razoável para português
MODEL_NAME = "ssmits/Falcon2-5.5B-Portuguese"

tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
model = AutoModelForCausalLM.from_pretrained(MODEL_NAME, torch_dtype=torch.float32)
pipe = pipeline("text-generation", model=model, tokenizer=tokenizer, device=0 if torch.cuda.is_available() else -1)

def montar_prompt(texto):
    return f"""
Dado a seguinte descrição de vaga de emprego:

\"\"\"{texto}\"\"\"

Extraia as informações da vaga acima em formato json com os campos "title", "required_skills", . Lembre-se que o campo techinical_skills é uma lista.
Não mostre mais nenhuma informação além do json
"""

def extrair_info(texto):
    prompt = montar_prompt(texto)
    print(prompt)
    resposta = pipe(prompt, max_new_tokens=256, do_sample=False)[0]["generated_text"]
    
    print(f"Resposta: {resposta}")

    # Extrai somente o JSON retornado (depois do prompt)
    splitado = resposta.split("{", 1)
    if len(splitado) < 2:
        return {}

    json_raw = "{" + splitado[1]
    try:
        # Pode precisar ajustar a limpeza dependendo do modelo
        return eval(json_raw)  # Para testar rapidamente (use json.loads com controle depois)
    except Exception as e:
        print("Erro ao interpretar JSON:", e)
        return {}
