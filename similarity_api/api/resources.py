from pydantic import BaseModel

class CollectionPointer(BaseModel):
    """Classe que define o formato do ponto (vetor) usado como referência
    para calcular os documentos similares
    """
    # Id do documento que possui o vetor de referência.
    id: int
    
    
class Document(BaseModel):
    """Classe que define o formato de resposta do Documento"""
    # Id único do documento
    id: int
    # Score de relevância em relção ao source (CollectionPointer)
    score: float


class SimilarityDocumentResponse(BaseModel):
    """Classe que define o formato de resposta da lista de documentos similares"""
    # Point Vector utilizado como referência para queries de similaridade
    source: CollectionPointer
    # Lista de documentos semelhantes
    similar_documents: list[Document]
    

class ResourceLink(BaseModel):
    """Classe que define o formato de resposta dos links da API"""
    # Endereço http do recurso.
    href: str
    # Definiçao curta do recurso.
    rel: str

    
class RootResource(BaseModel):
    """Classe que define o formato de endpoint raiz da API"""
    # Lista de Links acessíveis da API
    links :list[ResourceLink]
    
    
class IndexDocument(BaseModel):
    """Classe que define o formato do objeto utilizado para postar novos documentos
    via API. Esses documentos são indexados nas coleções do Qdrant
    """
    # Id único do documento
    id: int
    # Título do documento. Nome da Vaga ou Cargo do candidato
    title: str
    # Descrição da vaga ou um resumo do candidato
    description: str
    # Endereço da vaga ou do candidato
    location: str