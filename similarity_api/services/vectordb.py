from qdrant_client import QdrantClient
from qdrant_client.models import PointStruct
from configuration.environment import get_config
from api.resources import Document, IndexDocument
from configuration.logger import get_logger


logger = get_logger(__name__)
config = get_config()
client = QdrantClient(host=config.database.host, port=config.database.port)


weights = {
    "title": config.similarity.title,
    "description": config.similarity.description,
    "location": config.similarity.location
}

default_query_limit = 10

def get_similar_applicants(vacancy_id :int, limit :int) -> list[Document]:
    """
    Função que busca candidatos similares a partir de uma vaga no banco de vetores
    """
    points = client.retrieve(collection_name="vacancies", ids=[vacancy_id], with_vectors=True)
    
    if len(points) > 0:
        vacancy = points[0]
        applicants:list[Document] = []
        collection_name = "applicants"
        
        # Recupera os vetores do ponto base
        query_vectors = vacancy.vector

        # Realiza buscas separadas e acumula os scores
        scores = {}

        for field, weight in weights.items():
            results = client.search(
                collection_name=collection_name,
                query_vector=(field, query_vectors[field]),
                limit=default_query_limit
            )
            for r in results:
                if r.id not in scores:
                    scores[r.id] = 0
                scores[r.id] += r.score * weight

        # Ordena os resultados combinados
        sorted_results = sorted(scores.items(), key=lambda x: x[1], reverse=True )
        
        for point_id, score in sorted_results:
            applicants.append(Document(id=point_id, score=score))
        
        return applicants[:limit]
    else:
        return []
    
    
def get_similar_vacancies(applicant_id :int, limit :int) -> list[Document]:
    """
    Função que busca as vagas similares a partir de um candidato no banco de vetores
    """
    points = client.retrieve(collection_name="applicants", ids=[applicant_id], with_vectors=True)
    
    if len(points) > 0:
        applicant = points[0]
        vacancy :list[Document] = []
        collection_name = "vacancies"
        
        # Recupera os vetores do ponto base
        query_vectors = applicant.vector

        # Realiza buscas separadas e acumula os scores
        scores = {}

        for field, weight in weights.items():
            results = client.search(
                collection_name=collection_name,
                query_vector=(field, query_vectors[field]),
                limit=default_query_limit
            )
            for r in results:
                if r.id not in scores:
                    scores[r.id] = 0
                scores[r.id] += r.score * weight

        # Ordena os resultados combinados
        sorted_results = sorted(scores.items(), key=lambda x: x[1], reverse=True )
        for point_id, score in sorted_results:
            vacancy.append(Document(id=point_id, score=score))
        
        return vacancy[:limit]
    else:
        return []
    

def post_document(doc:dict, collection_name: str):
    """
    Função que envia o documento para o banco de Vetores
    """
    try:
        response = client.upsert(
            collection_name=collection_name,
            points=[
                PointStruct(
                    id=doc["id"],
                    vector={
                        "title":doc["title_embedding"],
                        "description": doc["description_embedding"],
                        "location": doc["location_embedding"],
                    },
                    payload={"title":doc["title"], "description": doc["description"], "location": doc["location"]}
                )
            ]
        )
        
        logger.info("Document indexed successfully.")
    except Exception as e:
        logger.error("Error on vector document indexing", e)
        raise e
