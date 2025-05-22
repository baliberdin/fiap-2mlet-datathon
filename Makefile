# Define o diretório raiz do projeto
PYTHONPATH := $(PWD)
$(echo PYTHONPATH)

# Task para rodar os testes
run-libraries-test:
	@PYTHONPATH=$(PWD) && pytest --disable-warnings data_transform_utilities

run-api-test:
	@PYTHONPATH=$(PWD) && cd ./similarity_api && pytest --disable-warnings

build-images:
	@docker build -t decision-app ./decision-app/
	@docker build -t similarity-api ./similarity_api/

start-all:
	@docker compose up -d

start-mlflow-server:
	@docker compose up -d mlflow-server

start-mysql-server:
	@docker compose up -d mysql

start-decision-app:
	@docker compose up -d decision-app

start-monitoring:
	@docker compose up -d prometheus grafana

start-similarity-api:
	@docker compose up -d similarity-api

run-mysql-client:
	docker exec -it mysql mysql -u decision -p

build-python-libraries:
	@python -m build data_transform_utilities

install-libraries:
	@pip install --force-reinstall ./data_transform_utilities

publish-libraries:
	@twine upload --repository-url http://localhost:8081/ ./data_transform_utilities/dist/*

run-similarity-api-without-docker:
	@cd similarity_api && fastapi run --reload ./main.py

rebuild-decision-app: build-images
	@docker compose down decision-app
	@docker compose up -d decision-app

rebuild-similarity-api: build-images
	@docker compose down similarity-api
	@docker compose up -d similarity-api

run-ndgc-evaluation:
	@jupyter nbconvert --to notebook --execute model/scripts/ndcg_evaluation.ipynb --output=_ndcg_evaluation.ipynb

run-model-train:
	@jupyter nbconvert --to notebook --execute model/scripts/model_train.ipynb --output=_model_train.ipynb
	
restore-database:
	@jupyter nbconvert --to notebook --execute data_engineering/preprocessing_data.ipynb --output=_preprocessing_data.ipynb

restore-vector-database:
	@jupyter nbconvert --to notebook --execute data_engineering/vectors_indexing.ipynb --output=_vectors_indexing.ipynb