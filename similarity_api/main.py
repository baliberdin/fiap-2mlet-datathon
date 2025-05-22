from fastapi import FastAPI
from prometheus_fastapi_instrumentator import Instrumentator
from prometheus_client import Gauge
import os
import pandas as pd
from configuration.logger import get_logger
from configuration.environment import get_config
from services.model import ModelService
from services import vectordb
from fastapi.exceptions import HTTPException
from fastapi.responses import Response
from api.resources import SimilarityDocumentResponse, CollectionPointer, RootResource, ResourceLink, IndexDocument

logger = get_logger(__name__)
# Carrega as configurações da aplicação
config = get_config()

# Inicia o framework FastAPI e adiciona o endpoint de métricas do Prometheus
app = FastAPI(title="Stock Predictions API")
instrumentator = Instrumentator().instrument(app).expose(app)
model_service = ModelService(model_name=config.model.name, model_version=config.model.version, mlflow_tracking_uri=config.model.mlflow_tracking_uri)


@app.get("/")
async def root() -> RootResource:
    """
        Função raiz da API de similaridade. Exibe os recursos disponíveis
        na API
        
        Returns:
            dict: JSON com a lista dos IDs dos candidatos similares
    """
    links :list[ResourceLink]= []
    links.append(ResourceLink(rel="similar_applicants",href="/similarity/applicants"))
    links.append(ResourceLink(rel="similar_vacancies",href="/similarity/vacancies"))
    root_resource = RootResource(links=links)
    return root_resource


@app.get("/similarity/applicants")
async def similar_applicants(vacancy_id:int, limit:int = 5) -> SimilarityDocumentResponse:
    """
        Função de similaridade entre vagas e candidatos que retorna candidatos similares a uma 
        determinada vaga
        
        Args:
            vacancy_id: int - ID da Vaga no banco de vetores
            limit:int - Quantidade de candidatos similares com a vaga
        Returns:configuration
            SimilarityDocumentResponse: JSON com a lista dos IDs dos candidatos similares e seus respectivos scores
    """
    
    try:
        pointer = CollectionPointer(id=vacancy_id)
        similar_applicants = vectordb.get_similar_applicants(pointer.id, limit*1)
        response = SimilarityDocumentResponse(similar_documents=similar_applicants, source=pointer)
        return response
    except Exception as e:
        logger.error(e)
        raise HTTPException(status_code=500)



@app.get("/similarity/vacancies")
async def similar_vacancies(applicant_id:int, limit:int = 5):
    """
        Função de similaridade entre vagas e candidatos que retorna vagas similares a um
        determinado candidato
        
        Args:
            applicant_id: int - ID da Vaga no banco de vetores
            limit:int - Quantidade de candidatos similares com a vaga
        Returns:
            SimilarityDocumentResponse: JSON com a lista dos IDs das vagas similares e seus respectivos scores
    """
    
    try:
        pointer = CollectionPointer(id=applicant_id)
        similar_vacancies = vectordb.get_similar_vacancies(pointer.id, limit*1)
        response = SimilarityDocumentResponse(source=pointer, similar_documents=similar_vacancies)
        return response 
    except Exception as e:
        logger.error(e)
        raise HTTPException(status_code=500)


@app.post("/document/{collection_name}")
async def index_document(doc:IndexDocument, collection_name:str):
    """Recurso que recebe um documento para indexado no Qdrant.
    Primeiro o embeddings devem ser calculados usando o Modelo treinado
    
    Args:
        doc: Document - Objeto contendo os campos do documento para indexação
        collection_name: str - Nome da coleção onde o documento deve ser indexado.
    """
    try:
        doc_vector = model_service.get_embedding(doc)
        vectordb.post_document(doc_vector, collection_name)
        return Response(status_code=201)
    except Exception as e:
        logger.error(e)
        raise HTTPException(status_code=500)