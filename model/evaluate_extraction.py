import json
from sklearn.metrics import precision_score, recall_score, f1_score
from extractor.hf_llm import extrair_info

def normalizar_lista(lista):
    return sorted([x.lower() for x in lista])

def comparar_habilidades(esperadas, preditas):
    esperadas = normalizar_lista(esperadas)
    preditas = normalizar_lista(preditas)
    conj_esp = set(esperadas)
    conj_pred = set(preditas)
    
    tp = len(conj_esp & conj_pred)
    fp = len(conj_pred - conj_esp)
    fn = len(conj_esp - conj_pred)

    return tp, fp, fn

def main():
    with open("datasets/golden_dataset.json") as f:
        exemplos = json.load(f)

    total_tp = total_fp = total_fn = 0
    titulos_corretos = 0

    for exemplo in exemplos:
        texto = exemplo["texto"]
        esperado = exemplo["esperado"]
        predito = extrair_info(texto)

        # Avaliar habilidades
        tp, fp, fn = comparar_habilidades(
            esperado["habilidades_necessarias"],
            predito.get("required_skills", [])
        )
        total_tp += tp
        total_fp += fp
        total_fn += fn

        # Avaliar título (match exato, case-insensitive)
        if predito.get("title", "").lower() == esperado["titulo"].lower():
            titulos_corretos += 1

    precision = total_tp / (total_tp + total_fp) if (total_tp + total_fp) else 0
    recall = total_tp / (total_tp + total_fn) if (total_tp + total_fn) else 0
    f1 = 2 * precision * recall / (precision + recall) if (precision + recall) else 0

    print("=== Avaliação de Extração ===")
    print(f"Habilidades - Precision: {precision:.2f}")
    print(f"Habilidades - Recall:    {recall:.2f}")
    print(f"Habilidades - F1-score:  {f1:.2f}")
    print(f"Títulos corretos:        {titulos_corretos}/{len(exemplos)}")

if __name__ == "__main__":
    main()
