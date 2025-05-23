import os
from functools import lru_cache

from pydantic import BaseModel
from pydantic_settings import SettingsConfigDict
from pydantic_settings_yaml import YamlBaseSettings

import logging

logger = logging.getLogger(__name__)


class VectorDatabaseConfig(BaseModel):
    """
    Classe que define a configuração de acesso ao banco de dados de vetores.
    """
    # endereço IP ou Hostname do servidor de banco de dados
    host: str
    # Porta em que o banco de dados recebe conexões
    port: int
    
class SimilarityWeightConfig(BaseModel):
    """
    Classe que define as configurações de peso dos vetores de similaridade
    """
    # Peso utilizado para o título
    title: float
    # Peso utilizado para a descrição
    description: float
    # Peso utilizado para a localização
    location: float
    

class ModelConfig(BaseModel):
    """Classe que representa as configurações do modelo"""
    # Nome do modelo publicado no Mlflow
    name: str
    # Versão do modelo publicado no mlflow
    version: int
    # URL do serviço do mlflow
    mlflow_tracking_uri: str
    # Número máximo de dias para predições
    max_preditions: int
            

    
class AppConfig(BaseModel):
    """
    Classe que define as configurações da API
    """
    # Nome da aplicação. Será exibida na tela de documentação /docs
    application_name: str
    # Configuração do acesso ao banco de dados
    database: VectorDatabaseConfig
    # Configurações do modelo
    model: ModelConfig
    # Configuração dos pesos de similaridade
    similarity: SimilarityWeightConfig
    

class SettingsLoader(YamlBaseSettings):
    """
    Classe que carrega as configurações gerais da aplicação exceto as configurações de log
    """
    # Atributo que guarda as configurações da aplicação
    app_config: AppConfig
    # Carrega as configurações a partir do arquivo env.yaml
    model_config = SettingsConfigDict(secrets_dir='./secrets', yaml_file='./env.yaml', env_file_encoding='utf-8')


@lru_cache
def get_config() -> AppConfig:
    """ Captura todas as configurações definidas em variáveis de ambiente ou no arquivo env.yaml
    Variáveis de ambiente tem precedência em relação às que estão no arquivo env.yaml
    Todas as configurações são cacheadas usando lru_cache

    Returns:
        AppConfig: Todas as configurações da aplicação
    """

    settings = SettingsLoader().app_config
    logger.debug(f"Configuration: {settings}")
    return settings