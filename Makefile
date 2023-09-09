# Makefile

# Variables
DC = docker-compose
DC_RUN = $(DC) run --rm app sh -c
MANAGE = $(DC_RUN) "python manage.py"

# Commands

## General
.PHONY: package pkg
package pkg:
	@echo "Not implemented yet"

## Docker
.PHONY: build b
build b:
	@$(DC) build

.PHONY: up u
up u:
	@$(DC) up

.PHONY: down d
down d:
	@$(DC) down

.PHONY: update u
update: create-migrations build

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
	@$(MANAGE) makemigrations

.PHONY: migrate m
migrate m:
	@$(MANAGE) migrate

.PHONY: create-superuser su
create-superuser su:
	@$(MANAGE) createsuperuser

.PHONY: startproject spr
startproject spr:
	$(eval ARGS := $(wordlist 2,$(words $(MAKECMDGOALS)),$(MAKECMDGOALS)))
	@$(if $(ARGS),,$(error You must specify project name))
	@$(DC_RUN) "django-admin startproject $(ARGS) ."

.PHONY: startapp sa
startapp sa:
	$(eval ARGS := $(wordlist 2,$(words $(MAKECMDGOALS)),$(MAKECMDGOALS)))
	@$(if $(ARGS),,$(error You must specify app name))
	@$(MANAGE) startapp $(ARGS)