from transformers import AutoModel, AutoTokenizer 
import torch 
import numpy as np 
from sklearn.metrics.pairwise import cosine_similarity


#model_name = 'bert-base-uncased' 
model_name = 'neuralmind/bert-base-portuguese-cased'
tokenizer = AutoTokenizer.from_pretrained(model_name, max_length=512, padding=True, truncation=True) 
print(tokenizer.__class__)
model = AutoModel.from_pretrained(model_name) 

def get_embedding(text): 
    """Gera o embedding do texto usando BERT."""
    print("Embedding\n")
    # Tokenize e adicione [CLS] e [SEP] tokens 
    #tokens = tokenizer.tokenize(text) 
    inputs = tokenizer(text, return_tensors="pt") 
    #tokens = ['[CLS]'] + tokens + ['[SEP]'] 
    # Converta para IDs 
    #input_ids = tokenizer.convert_tokens_to_ids(tokens) 
    # Crie tensores do PyTorch 
    #tensor_input_ids = torch.tensor([input_ids]) 
    
    attention_mask = inputs["attention_mask"]
    
    # Desative o cálculo de gradientes (não estamos treinando) 
    with torch.no_grad(): 
        # Obtenha a saída do modelo 
        #output = model(tensor_input_ids) 
        output = model(**inputs)
        # Use o embedding da camada CLS como representação do texto 
    embeddings = output.last_hidden_state[:, 0, :] 
    return embeddings.numpy() 
    
    

def find_best_matches(job_description, candidates): 
    """Encontra os candidatos que melhor se encaixam na vaga.""" 
    # Gere o embedding da descrição da vaga 
    job_embedding = get_embedding(job_description) 
    print(job_embedding.shape)
    # Crie embeddings para todos os candidatos 
    candidate_embeddings = [] 
    #for c in candidates:
    #    candidate_embeddings.extend(get_embedding(c['resume']) ) 
    [candidate_embeddings.extend(get_embedding(c['resume'])) for c in candidates]
    
    print(np.array(candidate_embeddings).shape)
    # Calcule a similaridade de cosseno entre a vaga e cada candidato 
    similarities = cosine_similarity(candidate_embeddings, job_embedding) 
    # Retorne os candidatos mais similares (maiores pontuações) 
    ranked_candidates = sorted(zip(candidates, similarities), key=lambda x: x[1], reverse=True) 
    return ranked_candidates

#job_description = "Procuramos um engenheiro de machine learning experiente em processamento de linguagem natural e deep learning." 
job_description = "Procuramos uma engenheira de machine learning experiente em processamento de linguagem natural e deep learning."
candidates = [ 
    {"id": 1, "name": "Alice", "resume": "Engenheira de ML com foco em NLP e experiência em transformers."},
    {"id": 2, "name": "Bob", "resume": "Desenvolvedor Python sênior com interesse em machine learning."},
    {"id": 3, "name": "Charlie", "resume": "Cientista de dados especializado em análise estatística."},
] 

#X = [[0, 0, 0]]
#Y = [[1, 0, 0], [1, 1, 0], [2, 2, 2]]
#print(cosine_similarity(X, Y))

best_matches = find_best_matches(job_description, candidates) 
print("Melhores candidatos:") 
#for candidate, score in best_matches: 
#    print(f"{candidate['name']}: {score:.4f}")
    
for m in best_matches: 
    print(m)
    
    
#import faiss                   # make faiss available
#index = faiss.IndexFlatL2(d)   # build the index
#print(index.is_trained)
#index.add(xb)                  # add vectors to the index
#print(index.ntotal)
    