import re 
import json

def clean_str(str :str):
    new_str = str
    str = str.lower().strip()
    
    while True:
        
        # Remove espacos em branco extras
        str = re.sub(r'\s+', ' ', str).strip()
        
        # Remove caracteres especiais no início e no final da string
        str = re.sub(r'(^([^a-zA-Z0-9A-zÀ-ú])+)|(([^a-zA-Z0-9A-zÀ-ú])+$)', '', str).strip()
        
        # Remove números entre parênteses
        str = re.sub(r'\(\d+\)', '', str).strip()
        #str = re.sub(r'\d+\/\d+', '', str).strip()
        
        # Remove codigos de vagas no final da string
        #str = re.sub(r'-\s+[a-z]+\d+$', '', str).strip()
        #str = re.sub(r'-\s+[a-z]+[\-_]\d+$', '', str).strip()
        
        #str = re.sub(r'\s?((\d+\/\d+)|(([a-z]{0,3})(_)?\d+(_\d+)?)|(\d+_\d+))$', '', str).strip()
        str = re.sub(r'\s((\d+\/\d+)|(([a-z]{0,3})([\-_])?\d+([\-_]\d+)?)|(\d+[\-_]\d+))$', '', str).strip()
        
        str = re.sub(r'\s-([a-z]{0,3})-\d+_\d+$', '', str).strip()
        
        
        # Remove numeros no final da string
        str = re.sub(r'\d+$', '', str).strip()
        
        # Remove números no início da string
        str = re.sub(r'^\d+', '', str).strip()
        
        # Remove hiphen no início e no final da string
        str = re.sub(r'^-\s+', '', str).strip()
        str = re.sub(r'\s+-(\s+)?$', '', str).strip()
        
        #str = re.sub(r'\s+-([a-z])+-?$', '', str).strip()
        
        #remove caracteres especiais
        str = re.sub(r'[^a-z0-9\s\-\/\.\&\–A-zÀ-ú]+', '', str).strip()
        
        str = re.sub(r'\s-[a-z]+$', '', str).strip()
        
        str = re.sub(r'\s+', ' ', str).strip()
        
        if str == new_str:
            break
        new_str = str
        
    return str

def extract_json(texto): 
    padrao = r"```json(.*?)```" 
    match = re.search(padrao, texto.replace('\n', ' ')) 

    if match: 
        return json.loads(match.group(1).strip())
    else: 
        return None
    
def json_str_to_array(json_str :str):
    if not json_str:
        return None
    
    if not re.match(r'^\[.*\]$', json_str):
        return [json_str]
    
    obj = json.loads(json_str)
    items = []
    for v in obj:
        if isinstance(v, list):
            items.extend(v)
        else:
            items.append(v)
    return items

def _flat_map(f, xs):
    ys = []
    for x in xs:
        ys.extend(f(x))
    return ys

def normalize_and_tokenize_text(text :str):
    if not text: return None
    
    new_text = text.lower().strip()
    new_text = re.sub(r' +',' ',new_text)
    new_text = re.sub(r'[^a-z0-9À-ú \.,\:\-\_\#\@\n]', '', new_text)
    tokens = []
    
    separators = ['\n', '.', ',', ':', ' - ']
    for s in separators:
        if len(tokens) == 0:
            tokens.extend(list(filter(lambda x: len(x) > 0, map(lambda x: x.strip(), new_text.split(s)) ) ))
        else:
            new_tokens = []
            for t in tokens:
                new_tokens.extend(t.split(s))
            tokens = list(filter(lambda x: len(x) > 0,map(lambda x: x.strip(), new_tokens)))
    
    return tokens