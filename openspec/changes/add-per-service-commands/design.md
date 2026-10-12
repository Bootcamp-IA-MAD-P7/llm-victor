## Context

Ver [proposal.md](proposal.md) — Why. El estado actual y las restricciones que condicionan el enfoque:

- El `Makefile` ya tiene los comandos del conjunto (`help`, `build`, `pull`, `up`, `down`, `restart`, `ps`, `logs` y `check`) que dejó la historia [#8](https://github.com/Glezino/ai-content-generator/issues/8).
- `docker-compose.yml` levanta `frontend` y `api` (con `build`) y `qdrant` (imagen oficial con el volumen nombrado `qdrant-data`).
- [ARCHITECTURE §7](/docs/ARCHITECTURE.md#7-entorno-local-y-operación) fija la convención de nombres con los ejemplos `make up-api`, `make pull-qdrant` y `make logs-frontend`.
- Las recetas solo pueden invocar `docker compose`, sin sintaxis exclusiva de Bash, para funcionar con GNU Make en Windows, macOS y Linux.

## Goals / Non-Goals

**Goals:**

- Operar cada servicio por separado sin tocar los demás.
- Borrar los volúmenes solo con un comando separado y explícito.

**Non-Goals:**

- Cambiar los comandos globales ni el `docker-compose.yml`.
- Limpiar artefactos de build o imágenes: no está en el alcance de la historia.
- El comando de ingesta de RAG: llega con I4.

## Decisions

### 1. Convención `<operación>-<servicio>`

Cada target es `<operación>-<servicio>` con las operaciones `build` o `pull`, `up`, `down`, `restart`, `ps`, `logs` y `shell`. Sigue los ejemplos de ARCHITECTURE §7 y hace evidente el servicio afectado.

### 2. Qdrant usa `pull` en lugar de `build`

`frontend` y `api` tienen `build-<servicio>` porque se construyen desde su Dockerfile; `qdrant` tiene `pull-qdrant` porque usa la imagen oficial. `up-qdrant` no lleva `--build`.

*Alternativa:* dar a los tres las dos operaciones. Se descarta porque `qdrant` no se construye y `frontend`/`api` se descargan solo de forma indirecta.

### 3. Targets explícitos por servicio

Se escriben los targets uno a uno, agrupados por servicio, en lugar de reglas de patrón (`up-%`, `logs-%`…).

*Alternativa:* reglas de patrón, más cortas. Se descartan porque también capturan nombres no previstos (`make up-foo` intentaría `docker compose up foo`) y porque el conjunto de servicios es fijo y pequeño; la versión explícita mapea directo con las tareas de la historia y con el estilo actual del `Makefile`.

### 4. Borrado de volúmenes separado y explícito

`clean-volumes` ejecuta `docker compose down --volumes`. Ningún otro target borra volúmenes: `down` y `down-<servicio>` los conservan, y `make help` y ARCHITECTURE §7 marcan `clean-volumes` como destructivo.

### 5. `down-<servicio>` detiene y elimina solo ese servicio

`docker compose down <servicio>` (Compose v2) detiene y elimina el contenedor indicado y deja intactos los demás y los volúmenes; la red se mantiene porque siguen usándola los otros servicios.

### 6. La consola usa `sh`

`shell-<servicio>` ejecuta `docker compose exec <servicio> sh`. `sh` existe en las tres imágenes (se comprobó en `frontend`, `api` y `qdrant`), así que no hace falta un intérprete distinto por servicio.

## Risks / Trade-offs

- [Borrar volúmenes elimina los datos de Qdrant sin confirmación] → El target se llama `clean-volumes`, se documenta como destructivo en `make help` y ARCHITECTURE §7, y ningún otro comando borra volúmenes.
- [`shell-<servicio>` falla si el contenedor no está arrancado] → Esperado: `docker compose exec` requiere el servicio en marcha; el mensaje de Compose lo indica.
- [Repetición de recetas entre los tres servicios] → Aceptada a cambio de claridad y de no capturar targets no previstos (decisión 3).
