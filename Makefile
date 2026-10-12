# Comandos del proyecto (docs/ARCHITECTURE.md §7). Requieren Docker y GNU Make.
# Las recetas solo invocan docker compose para funcionar igual en Windows, macOS y Linux.
COMPOSE := docker compose

.DEFAULT_GOAL := help
.PHONY: help build pull up down restart ps logs check check-frontend check-api

help:
	$(info Uso: make COMANDO)
	$(info make build     Construye las imágenes de la web y la API)
	$(info make pull      Descarga las imágenes que no se construyen)
	$(info make up        Arranca web, API y Qdrant y espera a que estén sanos)
	$(info make down      Detiene los servicios y conserva los datos)
	$(info make restart   Reinicia los servicios)
	$(info make ps        Muestra el estado de los servicios)
	$(info make logs      Muestra los logs de los servicios)
	$(info make check     Ejecuta los checks de calidad de la web y la API)
	@exit 0

build:
	$(COMPOSE) build

pull:
	$(COMPOSE) pull --ignore-buildable

up:
	$(COMPOSE) up -d --build --wait

down:
	$(COMPOSE) down

restart:
	$(COMPOSE) restart

ps:
	$(COMPOSE) ps

logs:
	$(COMPOSE) logs -f --tail=100

check: check-frontend check-api

check-frontend:
	$(COMPOSE) run --rm --no-deps frontend npm run check

check-api:
	$(COMPOSE) run --rm --no-deps api sh -c "ruff check . && ruff format --check . && mypy && pytest"
