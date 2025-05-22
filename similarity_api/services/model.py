import mlflow
from configuration.logger import get_logger
from api.resources import IndexDocument


logger = get_logger(__name__)

class ModelService():
    """
    Classe que define a forma como nos comunicamos com os Modelos.
    Responsável por acessar o MLFlow server, carregar o modelo e realizar algumas chamadas para ele.
    """
    
    _instance = None
    
    def __new__(cls, *args, **kwargs):
        """
        Método que previne múltiplas instâncias dessa classe. (Singleton)
        """
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        else:
            logger.info("ModelService has already been created")
        return cls._instance
    
    def __init__(self,model_name, model_version, mlflow_tracking_uri):
        self._instance = self
            
        self.MLFLOW_TRACKING_URI = mlflow_tracking_uri
        self.MODEL_NAME = model_name
        self.MODEL_VERSION_NUMBER = model_version
        logger.info(f"MLFlow Model defined as [name:{self.MODEL_NAME} version:{self.MODEL_VERSION_NUMBER}]")
        
        logger.info("Loading ML Model...")
        self.load_model()
        logger.info("ML Model successfuly loaded.")
        
    
    def load_model(self):
        """
        Método que carrega o modelo do MLflow Server
        """
        mlflow.set_tracking_uri(self.MLFLOW_TRACKING_URI)
        self.model = mlflow.sentence_transformers.load_model(f"models:/applicant_job_similarity/{self.MODEL_VERSION_NUMBER}")
        
    
    def get_embedding(self, doc:IndexDocument):
        """
        Método que cria os embeddings do documento
        """
        try:
            doc_vector = {"id": doc.id}
            doc_vector["title_embedding"] = self.model.encode(doc.title, normalize_embeddings=True)
            doc_vector["description_embedding"] = self.model.encode(doc.description, normalize_embeddings=True)
            doc_vector["location_embedding"] = self.model.encode(doc.location, normalize_embeddings=True)
            
            doc_vector["title"] = doc.title
            doc_vector["description"] = doc.description
            doc_vector["location"] = doc.location
            
            return doc_vector
        except Exception as e:
            logger.error(e)
