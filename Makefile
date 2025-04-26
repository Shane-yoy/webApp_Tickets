# Makefile pour automatiser les commandes Flask et les tests

# Variables
APP_NAME = flask_app
DOCKER_COMPOSE = docker-compose
PYTHON = python

# Commandes
install:
	docker exec -it $(APP_NAME) pip install -r requirements.txt

run:
	docker exec -it $(APP_NAME) flask run --host=0.0.0.0 --port=5000

test:
	docker exec -it $(APP_NAME) pytest

lint:
	docker exec -it $(APP_NAME) flake8 app tests

coverage:
	docker exec -it $(APP_NAME) pytest --cov=app tests/

rebuild:
	docker-compose down
	docker-compose up --build

# Helpers
help:
	@echo "Commandes disponibles :"
	@echo "  make install   => Installe les dépendances dans le container"
	@echo "  make run       => Lance l'application Flask"
	@echo "  make test      => Lance les tests unitaires"
	@echo "  make lint      => Vérifie la qualité du code (flake8 nécessaire)"
	@echo "  make coverage  => Mesure la couverture de tests"
	@echo "  make rebuild   => Reconstruit entièrement les containers"
