# Makefile

default: help

# Variables
DC = docker-compose
DC_RUN = $(DC) run --rm app sh -c

# Commands

## General
.PHONY: package pkg
package pkg:
	@echo "Not implemented yet"

.PHONY: shell sh
shell sh:
	@$(DC_RUN) "python manage.py shell"

## Docker
.PHONY: build
build:
	@$(DC) build

.PHONY: up
up:
	@$(DC) up

.PHONY: down
down:
	@$(DC) down

.PHONY: update u
update u: create-migrations build

.PHONY: docker-clean-all dca
docker-clean-all dca:
	@echo "Removing all docker containers and images"
	@docker system prune --all

.PHONY: docker-clean-volume dcv
docker-clean-volume dcv:
	@echo "Removing all docker volumes"
	@docker volume prune

## Django

.PHONY: create-migrations cm
create-migrations cm:
	@$(DC_RUN) "python manage.py makemigrations"

.PHONY: migrate m
migrate m:
	@$(DC_RUN) "python manage.py migrate"

.PHONY: create-superuser su
create-superuser su:
	@$(DC_RUN) "python manage.py createsuperuser"

.PHONY: startproject spr
startproject spr:
	$(eval ARGS := $(wordlist 2,$(words $(MAKECMDGOALS)),$(MAKECMDGOALS)))
	@$(if $(ARGS),,$(error You must specify project name))
	@$(DC_RUN) "django-admin startproject $(ARGS) ."

.PHONY: startapp sa
startapp sa:
	$(eval ARGS := $(wordlist 2,$(words $(MAKECMDGOALS)),$(MAKECMDGOALS)))
	@$(if $(ARGS),,$(error You must specify app name))
	@$(DC_RUN) "python manage.py startapp $(ARGS)"

.PHONY: test t
test t:
	@echo "Running tests..."
	$(DC_RUN) "python manage.py test && flake8"

# pip install djangorestframework-simplejwt
# Command for install packages dynamically
# .PHONY: install i
# install i:
# 	$(eval ARGS := $(wordlist 2,$(words $(MAKECMDGOALS)),$(MAKECMDGOALS)))
# 	@$(if $(ARGS),,$(error You must specify package name))
# 	@echo "Installing $(ARGS)..."
# 	@$(DC_RUN) "pip install $(ARGS)"

# .PHONY: save s
# save s:
# 	@echo "Saving packages..."
# 	@$(DC_RUN) "pip freeze > requirements.txt"

# Help
.PHONY: help
help:
	@echo "Usage: make [command]"
	@echo ""
	@echo "Commands:"
	@echo "  build                     Build docker image"
	@echo "  up                        Start docker containers"
	@echo "  down                      Stop docker containers"
	@echo "  update, u                 Make migrations and build docker image"
	@echo "  docker-clean-all, dca     Remove all docker containers and images"
	@echo "  docker-clean-volume, dcv  Remove all docker volumes"
	@echo "  create-migrations, cm     Create migrations"
	@echo "  migrate, m                Apply migrations"
	@echo "  create-superuser, su      Create superuser"
	@echo "  startproject, spr         Create django project"
	@echo "  startapp, sa              Create django app"
	@echo "  help                      Show this help message and exit"

