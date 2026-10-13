## Context

Ver [proposal.md](proposal.md) — Why. El estado actual y las restricciones que condicionan el enfoque:

- `app/config.py` (`Settings`, pydantic-settings) ya lee del entorno `CORS_ORIGINS`, `GROQ_API_KEY`, `OPENROUTER_API_KEY`, `OPENROUTER_MODEL` y `TEXT_MODELS`. `create_app(settings)` permite inyectar la configuración en los tests.
- La API no usa Qdrant. En Compose, `qdrant` corre en la misma red, pero la API no recibe su dirección. [ARCHITECTURE §3](/docs/ARCHITECTURE.md#3-componentes) lo marca como «Actual: sin uso todavía».
- `backend/Dockerfile` solo tiene `base` (Python 3.13 slim con uv y el venv en `/opt/venv`) y `dev` (`uv sync --frozen`, `uvicorn --reload`, puerto 8000).
- El contrato [API HTTP](/docs/CONTRACTS/api.md) (0.8.0) dice que `GET /health` no comprueba dependencias externas. La web lo consulta para su indicador de disponibilidad.
- Plataformas como Railway inyectan el puerto en `PORT` y pasan la configuración como variables del servicio ([ARCHITECTURE §9](/docs/ARCHITECTURE.md#9-despliegue)).

## Goals / Non-Goals

**Goals:**

- Comprobar desde la API, con la configuración real, si llega a Qdrant (local o externo, con o sin clave).
- Una imagen de producción de la API que se configure entera en tiempo de ejecución.

**Non-Goals:**

- Colecciones, ingesta o recuperación en Qdrant: llegan con I4.
- Cambiar `GET /health` o el indicador de la web.
- Unificar cómo leen el entorno los proveedores (`groq.py`, `openrouter.py` usan `os.getenv` como respaldo): ya funciona por entorno y sería un refactor ajeno a la historia.
- Exigir `CORS_ORIGINS` en producción: el valor por defecto (`http://localhost:5173`) solo bloquea orígenes ajenos, así que un olvido no abre la API. Se documenta como variable obligatoria del hosting.

## Decisions

### 1. Configuración de Qdrant en `Settings`

Se añaden `qdrant_url` (por defecto `http://localhost:6333`, para ejecutar la API fuera de Compose) y `qdrant_api_key` (vacía = sin clave). Compose define `QDRANT_URL=http://qdrant:6333` para la API. No hay más variables: la URL incluye esquema, host y puerto, que es lo que piden Qdrant Cloud y una instancia propia.

### 2. Cliente oficial `qdrant-client`

La comprobación usa `AsyncQdrantClient(url, api_key, timeout=…)` y `get_collections()`. Con eso se comprueba a la vez que Qdrant es accesible y que la clave es válida, porque `/readyz` no exige clave y no detectaría una clave incorrecta. El cliente se abre y se cierra en cada consulta: es una comprobación puntual y no compensa mantener un estado compartido antes de I4.

*Alternativa:* una petición `httpx` a la API REST de Qdrant. Evita una dependencia, pero I4 necesitará el cliente igualmente. El cliente añade peso a la imagen, un coste aceptado.

### 3. Endpoint `GET /health/qdrant`

- `200 OK` con `{"status": "ok"}` si Qdrant responde y acepta la clave.
- `503 Service Unavailable` con `{"detail": "Qdrant no está disponible"}` ante cualquier error: timeout, conexión rechazada, URL mal formada o `401`/`403`. La causa se registra en el log de la API y no se devuelve.
- Timeout corto (3 s), para no colgar la petición.

La comprobación vive en una función que el endpoint recibe como dependencia de FastAPI. Así los tests la sustituyen sin red. `GET /health` no se toca. El contrato sube a 0.9.0 (MINOR, endpoint nuevo).

*Alternativa:* incluir Qdrant en `/health`. Se descarta porque cambiaría el contrato existente y lo que la web muestra, y Qdrant aún no es necesario para generar.

### 4. Etapa `prod` en el Dockerfile

Desde `base`: `uv sync --frozen --no-dev` y se copia solo `app/`. Se ejecuta con un usuario sin privilegios creado en la imagen. El comando es `uvicorn app.main:app --host 0.0.0.0 --port ${PORT}`, con `ENV PORT=8000`, en forma shell con `exec` para que uvicorn reciba las señales. Es la última etapa, así que se construye por defecto sin `--target`. `dev` no cambia.

### 5. `make image-api` y CI

`make image-api` ejecuta `docker build --target prod -t ai-content-studio-api:prod backend`, igual que `image-frontend`. El job `API` del CI añade un paso que construye la imagen sin publicarla.

### 6. Tests

- **Unitarios:** `Settings` lee `QDRANT_URL` y `QDRANT_API_KEY`. El endpoint responde 200 o 503 según la comprobación sustituida, y el 503 no contiene la clave ni el mensaje del error. La función de comprobación devuelve «no disponible» ante una excepción del cliente, que se simula.
- **Integración manual:**
  - La API de Compose contra el Qdrant local.
  - La imagen `prod` contra un Qdrant «externo»: un contenedor aparte con `QDRANT__SERVICE__API_KEY`, en otra red, conectado solo por URL y clave. Se prueba con la clave correcta (200), con una incorrecta (503) y con Qdrant parado (503).
  - El puerto por `PORT` y la configuración de CORS en la imagen.

## Risks / Trade-offs

- [`qdrant-client` amplía la imagen y las dependencias] → Aceptado: I4 lo necesitará. La versión queda fijada en `uv.lock`.
- [El cliente avisa al usar una clave sobre `http`] → Es solo un aviso en el log. En producción se usará `https`; se documenta.
- [Un fallo de Qdrant no se ve en la web] → Fuera de alcance: la web no depende de Qdrant hasta I4.

## Migration Plan

Sin migración. Quien tenga un `.env` propio no necesita cambiarlo: Compose define `QDRANT_URL`. Revertir es retirar el endpoint, la dependencia y la etapa `prod`.
