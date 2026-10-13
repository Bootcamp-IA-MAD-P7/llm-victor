## 1. Conexión a Qdrant por configuración

- [x] 1.1 Añadir `qdrant-client` con `uv add` y verificar que `uv.lock` se actualiza y `make build-api` funciona.
- [x] 1.2 Escribir primero los tests de `Settings` (`QDRANT_URL`, `QDRANT_API_KEY` y sus valores por defecto) y añadir los campos; verificar con `make check-api`.
- [x] 1.3 Escribir primero los tests de la comprobación (disponible, excepción del cliente → no disponible) y del endpoint `GET /health/qdrant` (200; 503 sin clave ni detalle interno; `/health` sigue en 200 aunque Qdrant falle), e implementarlos; verificar con `make check-api`.
- [x] 1.4 Definir `QDRANT_URL=http://qdrant:6333` para la API en `docker-compose.yml`; verificar con `make up` que `GET /health/qdrant` responde 200 y, con `make down-qdrant`, 503.

## 2. Imagen de producción

- [x] 2.1 Añadir al `Dockerfile` la etapa `prod` (`uv sync --frozen --no-dev`, solo `app/`, usuario sin privilegios, puerto de `PORT` con 8000 por defecto) sin tocar `dev`; verificar que `docker build --target dev` sigue funcionando.
- [x] 2.2 Añadir `make image-api` (con su `.PHONY` y su línea en `make help`); verificar que construye la imagen sin Compose, que corre sin root, que responde en `PORT` y en 8000 por defecto, y que aplica `CORS_ORIGINS` del entorno.
- [x] 2.3 Comprobar la imagen contra un Qdrant externo: un contenedor aparte con clave, conectado solo por `QDRANT_URL` y `QDRANT_API_KEY`; verificar 200 con la clave correcta, 503 con una incorrecta y 503 con Qdrant parado.

## 3. CI

- [x] 3.1 Añadir al job `API` de `.github/workflows/ci.yml` la construcción de la imagen `prod`; verificar en el CI del PR.

## 4. Documentación

- [x] 4.1 Actualizar el [contrato de la API](/docs/CONTRACTS/api.md) a 0.9.0 con `GET /health/qdrant`; verificar que `/health` sigue documentado sin cambios.
- [x] 4.2 Actualizar ARCHITECTURE §3 (estado de `qdrant`), §6 (conexión a Qdrant por entorno), §7 (`make image-api`) y §9 (imagen de la API, variables obligatorias del hosting —`CORS_ORIGINS`, claves de proveedores, `QDRANT_URL`, `QDRANT_API_KEY` y `PORT`— y `https` para Qdrant con clave), y `.env.example`; verificar que no queda ninguna referencia contradictoria.
