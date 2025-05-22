from fastapi.testclient import TestClient
from unittest.mock import patch
from main import app
from services.vectordb import get_similar_applicants
from api.resources import SimilarityDocumentResponse, CollectionPointer, Document
from fastapi.exceptions import HTTPException


client = TestClient(app)

def test_should_return_available_endpoints_on_root():
    # When
    response = client.get("/")
    
    # Then
    assert response.status_code == 200
    assert response.json() == {"links": 
        [{"href": "/similarity/applicants","rel": "similar_applicants"},
        {"href": "/similarity/vacancies","rel": "similar_vacancies"}]}
    

@patch("services.vectordb.get_similar_applicants")
def test_should_return_empty_list_when_document_not_found(mock_service):
    # Given
    similar_documents :list[Document] = []
    mock_service.return_value = similar_documents
    
    # When
    response = client.get("/similarity/applicants?vacancy_id=1")
    
    # Then
    assert response.status_code == 200
    assert response.json() == {'similar_documents': [], 'source': {'id': 1}}
    

@patch("services.vectordb.get_similar_applicants")
def test_should_return_error_when_no_vacancy_id_was_defined(mock_service):
    # Given
    mock_service.return_value = {}
    
    # When
    response = client.get("/similarity/applicants")
    
    # Then
    assert response.status_code == 422
    assert response.json() == {
        "detail": [{
            "type": "missing",
            "loc": [
                "query",
                "vacancy_id"
            ],
            "msg": "Field required",
            "input": None
        }]}


@patch("services.vectordb.get_similar_vacancies")
def test_should_return_error_when_no_applicant_id_was_defined(mock_service):
    # Given
    mock_service.return_value = {}
    
    # When
    response = client.get("/similarity/vacancies")
    
    # Then
    assert response.status_code == 422
    assert response.json() == {
        "detail": [{
            "type": "missing",
            "loc": [
                "query",
                "applicant_id"
            ],
            "msg": "Field required",
            "input": None
        }]}


@patch("services.vectordb.get_similar_applicants")
@patch("services.vectordb.get_similar_vacancies")        
def test_should_return_error_when_call_to_vectordb_fail(mock_vacancy_service, mock_applicant_service):
    # Given
    mock_vacancy_service.side_effect = Exception("Timedout")
    mock_applicant_service.side_effect = Exception("Timedout")
    
    # When
    response = client.get("/similarity/applicants?vacancy_id=1")
    response2 = client.get("/similarity/vacancies?applicant_id=1")
        
    # Then
    assert response.status_code == 500
    assert response2.status_code == 500
    assert response.json() == {"detail": "Internal Server Error"}
    assert response2.json() == {"detail": "Internal Server Error"}
    
    
@patch("services.vectordb.post_document")
@patch("main.model_service")
def test_should_embedding_document(mock_vectordb_service, mock_model_service):
    # Given
    doc = {"id":1, "title":"Dev Java", "description":"Conhecimento em Spring Boot", "location":"São Paulo, São Paulo"}
    
    # When
    response = client.post("/document/vacancies", json=doc)
    
    print(mock_vectordb_service)
    print(mock_model_service)
    
    # Then
    assert response.status_code == 201
    assert mock_model_service.get_embedding(doc)
    assert mock_vectordb_service.post_document(any, any)