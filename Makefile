# Define o diretório raiz do projeto
PYTHONPATH := $(PWD)
$(echo PYTHONPATH)

# Task para rodar os testes
run-libraries-test:
	PYTHONPATH=$(PWD) pytest data_transform_utilities

start-all: run-test
	@docker compose up -d

start-mlflow-server:
	docker compose up -d mlflow-server

run-mysql-client:
	docker exec -it mysql mysql -u decision -p

build-python-libraries:
	python -m build data_transform_utilities
	python -m build model

install-libraries:
	pip install --force-reinstall ./data_transform_utilities