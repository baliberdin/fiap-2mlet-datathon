def generate_score_from_status(status: str) -> float:
    """
    Função que gera um Score baseado em um Status do candidato que
    está concorrendo uma vaga. Quanto mais próximo de Contratado maior 
    o score.
    """
    if status is None or len(status.strip()) == 0:
        return 0 
    
    status_text = status.strip()
    
    hireds = [
        'Contratado pela Decision',
        'Contratado como Hunting',
        'Proposta Aceita',
        'Aprovado',
        'Documentação PJ',
        'Documentação CLT',
        'Documentação Cooperado',
        'Encaminhar Proposta',
    ]
    
    interviews = [
        'Entrevista Técnica',
        'Entrevista com Cliente',
        'Em avaliação pelo RH',
    ]
    
    applicants = [
        'Prospect',
        'Encaminhado ao Requisitante',
        'Inscrito',
    ]
    
    recused = [
        'Desistiu',
        'Sem interesse nesta vaga',
        'Desistiu da Contratação'
    ]
    
    reproved = [
        'Não Aprovado pelo Cliente',
        'Não Aprovado pelo RH',
        'Não Aprovado pelo Requisitante',
        'Recusado',
    ]
    
    if status_text in hireds: return 1
    if status_text in interviews: return 0.75
    if status_text in applicants: return 0.5
    if status_text in recused: return 0.25
    if status_text in reproved: return 0
    
    return 0
