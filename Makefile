# Comandos del proyecto (docs/ARCHITECTURE.md §7). Requieren Docker y GNU Make.
# Las recetas solo invocan docker y docker compose para funcionar igual en Windows, macOS y Linux.
COMPOSE := docker compose

.DEFAULT_GOAL := help
.PHONY: help build pull up down restart ps logs check check-frontend check-api \
	build-frontend up-frontend down-frontend restart-frontend ps-frontend logs-frontend shell-frontend \
	build-api up-api down-api restart-api ps-api logs-api shell-api \
	pull-qdrant up-qdrant down-qdrant restart-qdrant ps-qdrant logs-qdrant shell-qdrant \
	clean-volumes image-frontend

help:
	$(info Uso: make COMANDO)
	$(info )
	$(info Conjunto:)
	$(info make build         Construye las imágenes de la web y la API)
	$(info make pull          Descarga las imágenes que no se construyen)
	$(info make up            Arranca web, API y Qdrant y espera a que estén sanos)
	$(info make down          Detiene los servicios y conserva los datos)
	$(info make restart       Reinicia los servicios)
	$(info make ps            Muestra el estado de los servicios)
	$(info make logs          Muestra los logs de los servicios)
	$(info )
	$(info Por servicio (frontend, api, qdrant); cambia el sufijo, p. ej. make up-api:)
	$(info make build-<s>     Construye la imagen del servicio (frontend y api))
	$(info make pull-<s>      Descarga la imagen del servicio (qdrant))
	$(info make up-<s>        Arranca un servicio)
	$(info make down-<s>      Detiene y elimina un servicio, conservando los datos)
	$(info make restart-<s>   Reinicia un servicio)
	$(info make ps-<s>        Muestra el estado de un servicio)
	$(info make logs-<s>      Muestra los logs de un servicio)
	$(info make shell-<s>     Abre una consola en un servicio)
	$(info )
	$(info Datos:)
	$(info make clean-volumes  Borra contenedores, red y VOLÚMENES de datos (destructivo))
	$(info )
	$(info Calidad:)
	$(info make check         Ejecuta los checks de calidad de la web y la API)
	$(info )
	$(info Despliegue:)
	$(info make image-frontend VITE_API_URL=https://...  Construye la imagen de producción de la web)
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

# frontend

build-frontend:
	$(COMPOSE) build frontend

up-frontend:
	$(COMPOSE) up -d --build --wait frontend

down-frontend:
	$(COMPOSE) down frontend

restart-frontend:
	$(COMPOSE) restart frontend

ps-frontend:
	$(COMPOSE) ps frontend

logs-frontend:
	$(COMPOSE) logs -f --tail=100 frontend

shell-frontend:
	$(COMPOSE) exec frontend sh

# Imagen de producción, sin Compose; el build falla si falta VITE_API_URL.
image-frontend:
	docker build --target prod --build-arg VITE_API_URL=$(VITE_API_URL) -t ai-content-studio-frontend:prod frontend

# api

build-api:
	$(COMPOSE) build api

up-api:
	$(COMPOSE) up -d --build --wait api

down-api:
	$(COMPOSE) down api

restart-api:
	$(COMPOSE) restart api

ps-api:
	$(COMPOSE) ps api

logs-api:
	$(COMPOSE) logs -f --tail=100 api

shell-api:
	$(COMPOSE) exec api sh

# qdrant

pull-qdrant:
	$(COMPOSE) pull qdrant

up-qdrant:
	$(COMPOSE) up -d --wait qdrant

down-qdrant:
	$(COMPOSE) down qdrant

restart-qdrant:
	$(COMPOSE) restart qdrant

ps-qdrant:
	$(COMPOSE) ps qdrant

logs-qdrant:
	$(COMPOSE) logs -f --tail=100 qdrant

shell-qdrant:
	$(COMPOSE) exec qdrant sh

# datos

clean-volumes:
	$(COMPOSE) down --volumes
