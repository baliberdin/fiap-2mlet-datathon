import pandas as pd
from data_transform_utilities.src.text_parsers import clean_str, extract_json, json_str_to_array, normalize_and_tokenize_text
from io import StringIO
import json

def test_remove_numbers_within_parenthesis():
    # Given
    title = 'data&ai / application developer (13005587)'
    expected = 'data&ai / application developer'
    # When
    result = clean_str(title)
    # Then 
    assert result == expected, f"Expected: {expected}, but got: {result}"
    
def test_remove_numbers_and_especial_characteres_ent_end():
    # Given
    title =    'analista/desenvolvedor de sistema .net framework - 799/2021'
    expected = 'analista/desenvolvedor de sistema .net framework'
    # When
    result = clean_str(title)
    # Then 
    assert result == expected, f"Expected: {expected}, but got: {result}"
    
def test_remove_hiphen_at_end():
    # Given
    title =    'analista/desenvolvedor de sistema .net framework - '
    expected = 'analista/desenvolvedor de sistema .net framework'
    # When
    result = clean_str(title)
    # Then 
    assert result == expected, f"Expected: {expected}, but got: {result}"
    
def test_remove_vacancy_code_at_end():
    # Given
    title =    'consultor sap fi pleno - cf18189'
    expected = 'consultor sap fi pleno'
    # When
    result = clean_str(title)
    # Then 
    assert result == expected, f"Expected: {expected}, but got: {result}"
    
def test_remove_code_at_beginning():
    # Given
    title =    '3528017 - sap scm tm'
    expected = 'sap scm tm'
    # When
    result = clean_str(title)
    # Then 
    assert result == expected, f"Expected: {expected}, but got: {result}"
    
def test_remove_special_characters():
    # Given
    title =    '**desenvolvedor salesforce – sr - re-368741'
    expected = 'desenvolvedor salesforce – sr'
    # When
    result = clean_str(title)
    # Then 
    assert result == expected, f"Expected: {expected}, but got: {result}"
    
def test_should_preserve_accents():
    # Given
    title =    'Cloud Azure - Sênior - 11897444'
    expected = 'cloud azure - sênior'
    # When
    result = clean_str(title)
    # Then 
    assert result == expected, f"Expected: {expected}, but got: {result}"
    
def test_should_remove_codes_separated_by_hiphen():
    # Given
    title1 = 'Consultor Back-End . NetCore - 4806-1'
    title2 = 'Consultor Back-End . NetCore 4806-1'
    expected = 'consultor back-end . netcore'
    # When
    result1 = clean_str(title1)
    result2 = clean_str(title2)
    # Then 
    assert result1 == expected, f"Expected: {expected}, but got: {result1}"
    assert result2 == expected, f"Expected: {expected}, but got: {result1}"
    
def test_should_remove_codes_separated_by_underscore():
    # Given
    title1 = 'Dev Java – SR - RE-253968_1'
    title2 = 'Dev Java – SR - RE-253968_2'
    expected = 'dev java – sr'
    # When
    result1 = clean_str(title1)
    result2 = clean_str(title2)
    # Then 
    assert result1 == expected, f"Expected: {expected}, but got: {result1}"
    assert result2 == expected, f"Expected: {expected}, but got: {result1}"

def test_should_remove_other_types_of_codes():
    # Given
    title = 'especialista zabbix -re-309242'
    title2 = 'Oracle-Developer-2021-2596391'
    title3 = 'Consultor SAP MM PL -RE-291043_5'
    
    expected = 'especialista zabbix'
    expected2 = 'oracle-developer'
    expected3 = 'consultor sap mm pl'
    # When
    result = clean_str(title)
    result2 = clean_str(title2)
    result3 = clean_str(title3)
    # Then
    assert result == expected, f"Expected: {expected}, but got: {result}"
    assert result2 == expected2, f"Expected: {expected2}, but got: {result2}"
    assert result3 == expected3, f"Expected: {expected3}, but got: {result3}"
    
def test_should_extract_json():
    # Given
    source = '''```json
        {
        "title": "Configuration & Release Management",
        "requirements": [
            {
            "name": "5+ years' experience implementing .NET web applications, services and APIs",
            "significant_judgement": "comum"
            },
            {
            "name": "Expertise in .NET Core, microservices and modern cloud-based architectures",
            "significant_judgement": "incomum"
            },
            {
            "name": "Software development experience in any Cloud platform (Pivotal Cloud Foundry/Azure/AWS)",
            "significant_judgement": "comum"
            },
            {
            "name": "Experience implementing solutions with Angular",
            "significant_judgement": "incomum"
            },
            {
            "name": "Contribution in software engineering teams employing Agile/Lean principles and processes",
            "significant_judgement": "muito comum"
            },
            {
            "name": "Experience with Git source code control system",
            "significant_judgement": "muito comum"
            },
            {
            "name": "Proficiency with containers, orchestration technologies, and Continuous Integration (CI)/Continuous Delivery (CD) pipelines",
            "significant_judgement": "incomum"
            },
            {
            "name": "Experience maintaining automated tests",
            "significant_judgement": "comum"
            }
        ]
        }
        ```'''
    expected = '''{
        "title": "Configuration & Release Management",
        "requirements": [
            {
            "name": "5+ years' experience implementing .NET web applications, services and APIs",
            "significant_judgement": "comum"
            },
            {
            "name": "Expertise in .NET Core, microservices and modern cloud-based architectures",
            "significant_judgement": "incomum"
            },
            {
            "name": "Software development experience in any Cloud platform (Pivotal Cloud Foundry/Azure/AWS)",
            "significant_judgement": "comum"
            },
            {
            "name": "Experience implementing solutions with Angular",
            "significant_judgement": "incomum"
            },
            {
            "name": "Contribution in software engineering teams employing Agile/Lean principles and processes",
            "significant_judgement": "muito comum"
            },
            {
            "name": "Experience with Git source code control system",
            "significant_judgement": "muito comum"
            },
            {
            "name": "Proficiency with containers, orchestration technologies, and Continuous Integration (CI)/Continuous Delivery (CD) pipelines",
            "significant_judgement": "incomum"
            },
            {
            "name": "Experience maintaining automated tests",
            "significant_judgement": "comum"
            }
        ]
        }'''
    # When
    result = extract_json(source)
    # Then 
    assert json.dumps(result) == json.dumps(json.loads(expected)), f"Expected: {expected}, but got: {result}"
    
def test_should_parse_json_string_to_array():
    # Given
    json_array_str = '''["Experiência em Cloud Infrastructure Management (AWS, SAP BASIS, SQL, Oracle)","Experiência em entrega de serviços com cumprimento de SLAs","Habilidade para entender e resolver problemas técnicos complexos","Boas habilidades de delegação, negociação e gestão de pessoas","Excelentes habilidades de comunicação e relacionamento com clientes","Liderança em situações de crise e gerenciamento de incidentes"]'''
    expected = ['Experiência em Cloud Infrastructure Management (AWS, SAP BASIS, SQL, Oracle)',
                'Experiência em entrega de serviços com cumprimento de SLAs',
                'Habilidade para entender e resolver problemas técnicos complexos',
                'Boas habilidades de delegação, negociação e gestão de pessoas',
                'Excelentes habilidades de comunicação e relacionamento com clientes',
                'Liderança em situações de crise e gerenciamento de incidentes']
    # When
    result = json_str_to_array(json_array_str)
    # Then
    assert result == expected, f"Expected: {expected}, but got: {result}"
    assert len(result) == 6
    
def test_should_parse_string_to_array():
    # Given
    json_array_str = '''Experiência em Cloud Infrastructure Management (AWS, SAP BASIS, SQL, Oracle)'''
    expected = ['Experiência em Cloud Infrastructure Management (AWS, SAP BASIS, SQL, Oracle)']
    # When
    result = json_str_to_array(json_array_str)
    # Then
    assert result == expected, f"Expected: {expected}, but got: {result}"

def test_should_normalize_and_tokenize_text():
    # Given
    text = "Parágrafo inicial com ponto final.\n Exemplo de texto com: habilidades,  espaços    extras, e com formatação ruim, e com item vazio \n    \ntest" 
    expected = ["parágrafo inicial com ponto final","exemplo de texto com", "habilidades", "espaços extras", "e com formatação ruim", "e com item vazio", "test"]
    # When
    result = normalize_and_tokenize_text(text)
    # Then
    assert result == expected, f"Expected: {expected}, but got: {result}"           