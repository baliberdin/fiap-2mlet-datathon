from data_transform_utilities.score import generate_score_from_status

def test_should_define_score_zero_for_empty_status():
    # Given
    status = ''
    
    # When
    score = generate_score_from_status(status)
    
    # Then
    assert score == 0
    
def test_should_score_1_for_hired_status():
    # Given
    status = 'Contratado pela Decision'
    status2 = 'Contratado como Hunting'
    status3 = 'Proposta Aceita'
    status4 = 'Aprovado'
    status5 = 'Documentação PJ'
    status6 = 'Documentação CLT'
    status7 = 'Documentação Cooperado'
    status8 = 'Encaminhar Proposta'
    
    # When
    score = generate_score_from_status(status)
    score2 = generate_score_from_status(status2)
    score3 = generate_score_from_status(status3)
    score4 = generate_score_from_status(status4)
    score5 = generate_score_from_status(status5)
    score6 = generate_score_from_status(status6)
    score7 = generate_score_from_status(status7)
    score8 = generate_score_from_status(status8)
    
    # Then
    assert score == 1
    assert score2 == 1
    assert score3 == 1
    assert score4 == 1
    assert score5 == 1
    assert score6 == 1
    assert score7 == 1
    assert score8 == 1
    

def test_should_score_075_for_interview_status():
    # Given
    status = 'Entrevista Técnica'
    status2 = 'Entrevista com Cliente'
    status3 = 'Em avaliação pelo RH'
    
    # When
    score = generate_score_from_status(status)
    score2 = generate_score_from_status(status2)
    score3 = generate_score_from_status(status3)
    
    # Then
    assert score == 0.75
    assert score2 == 0.75
    assert score3 == 0.75
    

def test_should_score_050_for_prospects_and_applicants():
    # When
    status = 'Prospect'
    status2 = 'Encaminhado ao Requisitante'
    status3 = 'Inscrito'
    
    # When
    score = generate_score_from_status(status)
    score2 = generate_score_from_status(status2)
    score3 = generate_score_from_status(status3)
    
    # Then
    assert score == 0.5
    assert score2 == 0.5
    assert score3 == 0.5
    

def test_should_score_025_for_desistance():
    # When
    status =  'Desistiu'
    status2 = 'Sem interesse nesta vaga'
    status3 = 'Desistiu da Contratação'
    
    # When
    score = generate_score_from_status(status)
    score2 = generate_score_from_status(status2)
    score3 = generate_score_from_status(status3)
    
    # Then
    assert score == 0.25
    assert score2 == 0.25
    assert score3 == 0.25
    

def test_should_score_zero_for_reproveds():
    status  = 'Não Aprovado pelo Cliente'
    status2 = 'Não Aprovado pelo RH'
    status3 = 'Não Aprovado pelo Requisitante'
    status4 = 'Recusado'
    
    # When
    score = generate_score_from_status(status)
    score2 = generate_score_from_status(status2)
    score3 = generate_score_from_status(status3)
    score4 = generate_score_from_status(status4)
    
    # Then
    assert score == 0
    assert score2 == 0
    assert score3 == 0
    assert score4 == 0