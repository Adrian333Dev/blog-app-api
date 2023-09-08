# Makefile

# Variables
DC = docker-compose
DC_RUN = $(DC) run --rm app sh -c
MANAGE = $(DC_RUN) "python manage.py"


.PHONY: package pkg
package:
	@echo "Not implemented yet"
pkg: package

# Docker
.PHONY: build b
build:
	@echo "Building docker image"
	@$(DC) build
b: build

.PHONY: up u
up:
	@echo "Starting docker containers"
	@$(DC) up
u: up

.PHONY: down d
down:
	@echo "Stopping docker containers"
	@$(DC) down
d: down

.PHONY: update u
update: create-migrations build

.PHONY: docker-clean-all dca
docker-clean-all:
	@echo "Removing all docker containers and images"
	@docker system prune --all
dca: docker-clean-all

.PHONY: docker-clean-volume dcv
docker-clean-volume:
	@echo "Removing all docker volumes"
	@docker volume prune
dcv: docker-clean-volume

# 'C:\Program Files\Docker\Docker\Docker Desktop.exe'
.PHONY: docker-desktop dd
docker-desktop:
	@echo "Starting docker desktop"
	@start "" "C:\Program Files\Docker\Docker\Docker Desktop.exe"
dd: docker-desktop

# Django

## Migrations
.PHONY: create-migrations cm
create-migrations:
	@echo "Creating migrations"
	@$(MANAGE) makemigrations
cm: create-migrations

.PHONY: migrate m
migrate:
	@echo "Migrating"
	@$(MANAGE) migrate
m: migrate

## Django Entities
.PHONY: create-superuser su
create-superuser:
	@echo "Creating superuser"
	@$(MANAGE) createsuperuser
su: create-superuser

.PHONY: startproject spr
startproject:
	$(eval ARGS := $(wordlist 2,$(words $(MAKECMDGOALS)),$(MAKECMDGOALS)))
	@$(if $(ARGS),,$(error You must specify project name))
	@echo "Creating project: $(ARGS)"
	@$(DC_RUN) "django-admin startproject $(ARGS) ."
spr: startproject

.PHONY: startapp sa
startapp:
	$(eval ARGS := $(wordlist 2,$(words $(MAKECMDGOALS)),$(MAKECMDGOALS)))
	@$(if $(ARGS),,$(error You must specify app name))
	@echo "Creating app: $(ARGS)"
	@$(MANAGE) startapp $(ARGS)
sa: startapp
