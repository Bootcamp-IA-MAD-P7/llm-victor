## Why

La API ya lee CORS y las claves de los proveedores del entorno, pero no se puede alojar por separado. Su `Dockerfile` solo tiene la etapa de desarrollo, con `--reload`, dependencias de desarrollo y un puerto fijo. Tampoco sabe nada de Qdrant: no hay variables de conexión ni forma de comprobar que llega a una instancia externa. [ADR-0001](/docs/ADR/0001-docker-first-deployable-services.md) exige que cada servicio se despliegue por separado y se conecte a sus dependencias solo por configuración.

Historia [#20](https://github.com/Glezino/ai-content-generator/issues/20), épica [#7](https://github.com/Glezino/ai-content-generator/issues/7) (I1-E6), última historia abierta de la épica. Implementa RNF-05 y ADR-0001.

## What Changes

- La conexión a Qdrant se configura por entorno (`QDRANT_URL` y `QDRANT_API_KEY`, opcional). En Compose, la API apunta al Qdrant local.
- Nuevo endpoint `GET /health/qdrant`: indica si la API llega a Qdrant con la configuración actual. `GET /health` no cambia.
- El `Dockerfile` de la API gana una imagen de producción: sin recarga ni dependencias de desarrollo, sin root y con el puerto tomado de `PORT`.
- Nuevo comando `make image-api` que construye esa imagen por separado, sin Compose.
- El CI construye la imagen de producción de la API.
- Se documentan para un hosting futuro las variables de la API (CORS, secretos de proveedores, Qdrant y puerto) y la construcción de la imagen.
- CORS y los secretos de proveedores ya se leen del entorno: se verifican y se documentan, pero su código no cambia.
- **Fuera:** desplegar en un hosting, y usar Qdrant para RAG (I4).

## Capabilities

### New Capabilities

Ninguna.

### Modified Capabilities

- `deployable-services`: añade la imagen de producción de la API y su conexión a Qdrant por configuración, comprobable desde la API.

## Impact

- **API:** `app/config.py`, nuevo endpoint de salud de Qdrant, nueva dependencia `qdrant-client` y `Dockerfile` (etapa de producción); tests del endpoint y de la configuración.
- **Compose, Makefile y CI:** `QDRANT_URL` para la API, `make image-api` y construcción de la imagen en el job `API`.
- **Contrato:** [API HTTP](/docs/CONTRACTS/api.md) pasa a 0.9.0 (MINOR, endpoint nuevo).
- **Documentación:** ARCHITECTURE §3 (estado de `qdrant`), §6, §7 y §9, y `.env.example`.
- **Web:** sin cambios; no consume el nuevo endpoint.
- **ADR:** sin cambios; se aplica ADR-0001.
