## Context

No hay código: es el primer cambio. Lo fijan [ADR-0001](/docs/ADR/0001-docker-first-deployable-services.md) (Docker Compose, Makefile, servicios desplegables por separado) y [ARCHITECTURE](/docs/ARCHITECTURE.md) (§2 stack, §4 estructura y §7 operación). El equipo de desarrollo es Windows con Docker Desktop y GNU Make, y el producto debe funcionar también en macOS y Linux.

## Goals / Non-Goals

**Goals:**

- Que la persona solo necesite Docker y GNU Make para arrancar, operar y comprobar el proyecto.
- Iterar rápido: el código se recarga dentro de los contenedores al guardar.
- Dejar elegidas las herramientas de calidad que usarán todas las historias siguientes.

**Non-Goals:**

- Comandos por servicio y consola en un contenedor: [#11](https://github.com/Glezino/ai-content-generator/issues/11).
- Imágenes de producción y hosting: I1-E6.
- Conectar la API con Qdrant: llega con RAG (I4). Qdrant solo arranca y persiste datos.
- Crear los módulos `workflows`, `providers`, `knowledge` y `evaluation`: los crea la historia que los necesite.

## Decisions

### 1. Contenedores de desarrollo con recarga en caliente

Compose ejecuta los servidores de desarrollo (Vite y uvicorn con `--reload`) con el código montado desde el host. Cada Dockerfile es multi-stage y por ahora solo define el stage `dev`; el stage de producción llega en I1-E6.

*Alternativa:* construir ya la web estática y servirla con un servidor HTTP. Se descarta porque obliga a reconstruir la imagen en cada cambio y adelanta el trabajo de I1-E6.

### 2. Herramientas de `frontend`

npm con `package-lock.json` y Node 22 LTS. Vite con React y TypeScript; Tailwind CSS con su plugin de Vite; shadcn/ui inicializado, añadiendo componentes según se necesiten. Calidad: ESLint (la configuración de Vite, con reglas de React Hooks), Prettier, `tsc` para tipos y Vitest con Testing Library. Todo se expone como scripts de npm, incluido un `check` que los agrupa.

*Alternativas:* Oxlint, que create-vite 9 propone por defecto, y Biome, que reúne lint y formato en una sola herramienta. Se descartan porque ESLint tiene el ecosistema de reglas de React más maduro (React Hooks y React Refresh) y create-vite lo sigue ofreciendo con `--eslint`.

### 3. Herramientas de `api`

uv con `uv.lock` y Python 3.13. FastAPI con uvicorn, y configuración con pydantic-settings. Calidad: Ruff (lint y formato), mypy para tipos y pytest con el cliente de pruebas de FastAPI.

*Alternativas:* pip o Poetry; uv es más rápido y gestiona Python, el entorno virtual y el lockfile con una sola herramienta. Python 3.14 se descarta por ahora porque las librerías de embeddings que llegarán en I4 suelen tardar más en darle soporte.

### 4. La web llama a la API directamente y la API configura CORS

La web usa `VITE_API_URL`, una URL accesible desde el navegador del host (por defecto `http://localhost:8000`), y la API permite los orígenes de `CORS_ORIGINS`. El valor por defecto de `CORS_ORIGINS` se calcula a partir del puerto de la web, para que cambiar ese puerto no rompa la comunicación.

*Alternativa:* el proxy del servidor de desarrollo de Vite, que evita CORS en local pero esconde la configuración que exige el despliegue por separado (ADR-0001, consecuencias).

### 5. Salud y arranque ordenado

`GET /health` devuelve `200` con `{"status": "ok"}` y no comprueba dependencias, porque la API aún no usa ninguna. Cada servicio tiene un *healthcheck* en Compose con herramientas que ya trae su imagen (sin instalar curl). La web espera a que la API esté sana (`depends_on` con `service_healthy`), y `make up` usa `--wait` para terminar solo cuando todo está sano. La web comprueba la API al cargar, con un límite de 5 s para no quedarse esperando a una API que no responde, y ofrece un botón para reintentar.

Contrato: se registra `docs/CONTRACTS/api.md` en su versión `0.1.0`, con `GET /health`. La generación lo ampliará en [#9](https://github.com/Glezino/ai-content-generator/issues/9).

### 6. Configuración y secretos

Compose interpola cada variable con su valor por defecto (`${VAR:-valor}`), así que `.env` es opcional. `.env.example` documenta `FRONTEND_PORT`, `API_PORT`, `QDRANT_PORT`, `VITE_API_URL` y `CORS_ORIGINS`, sin secretos; la clave de Groq llega con #9.

### 7. Makefile como punto de entrada único

Targets: `help`, `build`, `pull`, `up`, `down`, `restart`, `ps`, `logs` y `check`. Las recetas solo invocan `docker compose`, sin sintaxis exclusiva de Bash, para que funcionen igual con GNU Make en Windows, macOS y Linux. `make check` ejecuta los checks dentro de los contenedores (`docker compose run --rm --no-deps`), así que el host no necesita ni Node ni Python.

### 8. CI

`ci.yml` añade los jobs `Frontend` y `API` junto a `OpenSpec`. Ejecutan las mismas herramientas en el runner, sin Docker, para aprovechar la caché de npm y uv y tardar menos.

### Sin ADR nuevo

Las herramientas de calidad y el diseño de los contenedores de desarrollo son decisiones locales y reversibles, así que basta con este documento. ARCHITECTURE §2, §3, §4, §7 y §8 se actualizan con lo que pasa a ser Actual.

## Risks / Trade-offs

- [En Windows, los cambios en archivos montados no siempre llegan al contenedor y la recarga no se dispara] → Activar el sondeo de archivos en Vite y en uvicorn mediante variables de entorno de Compose.
- [`node_modules` y el entorno virtual de Python chocan con el código montado desde el host] → `node_modules` en un volumen anónimo y el entorno de uv fuera del directorio montado (`UV_PROJECT_ENVIRONMENT`).
- [El primer `make up` tarda porque construye las imágenes] → Aceptado; los siguientes arranques reutilizan la caché.
- [Un puerto por defecto ya está ocupado en el equipo] → Todos los puertos se cambian en `.env`.
- [El CI ejecuta en el runner y `make check` en contenedores, así que podrían divergir] → Ambos usan los mismos scripts de npm, los mismos comandos de uv y los mismos lockfiles.
