.DEFAULT_GOAL := run
SETTINGS=parcelLab.settings

define HELP_FILE
Help
\033[32m install:\033[0m Install all dependencies

\033[32m migrations:\033[0m Generate migration files from models

\033[32m migrate:\033[0m Apply migration to database

\033[32m test:\033[0m Run tests for the application

\033[32m run:\033[0m Run application server

\033[32m startapp:\033[0m Create a new application (domain) within project \033[34m usage: make startapp app=app_name \033[0m

\033[32m setup:\033[0m Setup the project \033[31m this also clears your database\033[0m

endef
export HELP_FILE

# loads environment vars into shell context
-include .env
export $(shell sed 's/=.*//' .env)

help:
	clear
	@printf "$$HELP_FILE"

install: # Install all all dependencies
	@echo "Installing dependencies..."
	poetry install

installprecommits: # Install pre-commit hooks
	poetry run pre-commit install

setup: install migrate installprecommits seed # Setup the project

migrations: # Generate migration files from models
	poetry run python manage.py makemigrations

migrate: # Apply migration to database
	poetry run python manage.py migrate

run: # Run application server
	poetry run python manage.py runserver 0.0.0.0:8000

createsuperuser: # Interactive prompt to create a superuser
	poetry run django-admin createsuperuser

startapp: # Create a new application (domain) within project
	poetry run python manage.py startapp $(app)

test: install
	poetry run pytest -svv

seed:
	poetry run python manage.py seed
