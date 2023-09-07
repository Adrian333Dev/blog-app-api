# Makefile

# Variables
MANAGE = poetry run python -m core.manage

default: help


.PHONY: makemigrations mm
makemigrations:
	@echo "Making migrations"
	@$(MANAGE) makemigrations
mm: makemigrations

.PHONY: migrate m
migrate:
	@echo "Migrating"
	@$(MANAGE) migrate
m: migrate

.PHONY: add a
add:
	$(eval ARGS := $(wordlist 2,$(words $(MAKECMDGOALS)),$(MAKECMDGOALS)))
	@$(if $(ARGS),,$(error You must specify at least one argument))
	@echo "Adding following packages: $(ARGS)"
	@poetry add $(ARGS)
a: add

.PHONY: add-dev ad
add-dev:
	$(eval ARGS := $(wordlist 2,$(words $(MAKECMDGOALS)),$(MAKECMDGOALS)))
	@$(if $(ARGS),,$(error You must specify at least one argument))
	@echo "Adding following packages: $(ARGS)"
	@poetry add --group dev $(ARGS)
ad: add-dev

.PHONY: install i
install:
	@echo "Installing dependencies"
	@poetry install
i: install

remove:
	$(eval ARGS := $(wordlist 2,$(words $(MAKECMDGOALS)),$(MAKECMDGOALS)))
	@$(if $(ARGS),,$(error You must specify at least one argument))
	@echo "Removing following packages: $(ARGS)"
	@poetry remove $(ARGS)
rm: remove

install-pre-commit:
	@echo "Uninstalling and installing pre-commit"
	@poetry run pre-commit uninstall; poetry run pre-commit install
ipc: install-pre-commit


.PHONY: lint
lint:
	@echo "Running: pre-commit run --all-files"
	@poetry run pre-commit run --all-files
l: lint

.PHONY: update u
update: install migrate install-pre-commit;

.PHONY: runserver rs
runserver:
	@echo "Running server"
	@$(MANAGE) runserver
rs: runserver

.PHONY: run r
run:
	$(eval ARGS := $(wordlist 2,$(words $(MAKECMDGOALS)),$(MAKECMDGOALS)))
	@$(if $(ARGS),,$(MAKE) runserver)
	@echo "Running: $(ARGS)"
	@$(MANAGE) $(ARGS)
r: run

.PHONY: poetryrun pr
poetryrun:
	$(eval ARGS := $(wordlist 2,$(words $(MAKECMDGOALS)),$(MAKECMDGOALS)))
	@$(if $(ARGS),,$(error You must specify at least one argument))
	@echo "Running: $(ARGS)"
	@poetry run $(ARGS)
pr: poetryrun

.PHONY: flake8 f8
flake8:
	@echo "Running: flake8 $(ARGS)"
	@poetry run flakes $(ARGS)
f8: flake8

.PHONY: up-dependencies-only
up-dependencies-only:
	@echo "Starting dependencies"
	@$(if $(filter Windows_NT,$(OS)),(if not exist .env (echo. > .env)),(test -f .env || touch .env))
	docker-compose -f docker-compose.dev.yml up --force-recreate db
up-deps: up-dependencies-only

down-dependencies-only:
	@echo "Stopping dependencies"
	docker-compose -f docker-compose.dev.yml down
down-deps: down-dependencies-only

docker-desktop:
	@echo "Starting docker desktop"
	'C:\Program Files\Docker\Docker\Docker Desktop.exe'
dd: docker-desktop

.PHONY: superuser su
superuser:
	@echo "Creating superuser"
	@$(MANAGE) createsuperuser
su: superuser

.PHONY: help h
help:
	@echo "Usage: make <command>"
	@echo ""
	@echo "Commands:"
	@echo "  makemigrations, mm  Make migrations"
	@echo "  migrate, m          Migrate"
	@echo "  add, a              Add package"
	@echo "  add-dev, ad         Add package as dev dependency"
	@echo "  install, i          Install dependencies"
	@echo "  install-pre-commit  Uninstall and install pre-commit"
	@echo "  lint, l             Run pre-commit"
	@echo "  update, u           Install dependencies, migrate and install pre-commit"
	@echo "  runserver, rs       Run server"
	@echo "  run, r              Run command"
	@echo "  poetryrun, pr       Run command with poetry"
	@echo "  flake8, f8          Run flake8"
	@echo "  up-deps             Start dependencies"
	@echo "  docker-desktop, dd  Start docker desktop"
	@echo "  down-deps           Stop dependencies"
	@echo "  superuser, su       Create superuser"
	@echo "  help, h             Show this help message and exit"
