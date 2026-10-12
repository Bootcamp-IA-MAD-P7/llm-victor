## 1. API

- [x] 1.1 Crear `backend/` con uv (Python 3.13), FastAPI, pydantic-settings, Ruff, mypy y pytest; verificar que `uv sync` instala las dependencias y genera `uv.lock`.
- [x] 1.2 Implementar `GET /health` y la configuración por entorno (`CORS_ORIGINS`), con tests de la respuesta `200 {"status": "ok"}` y de las cabeceras CORS para un origen permitido y uno no permitido; verificar que pytest, Ruff y mypy pasan.
- [x] 1.3 Dockerfile multi-stage con el stage `dev` (uvicorn con `--reload` y el entorno de uv fuera del código montado); verificar que la imagen se construye.

## 2. Web

- [x] 2.1 Crear `frontend/` con Vite, React, TypeScript, Tailwind CSS y shadcn/ui, más ESLint, Prettier, Vitest y Testing Library, y los scripts `lint`, `format:check`, `typecheck`, `test`, `build` y `check`; verificar que `npm run check` y `npm run build` pasan.
- [x] 2.2 Página inicial que consulta `GET /health` en `VITE_API_URL` al cargar, con botón de reintento, y muestra «comprobando», «disponible» o «no disponible»; verificar con tests de componente de los estados «disponible» y «no disponible».
- [x] 2.3 Dockerfile multi-stage con el stage `dev` (servidor de Vite, `node_modules` en volumen y sondeo de archivos); verificar que la imagen se construye.

## 3. Compose y Makefile

- [x] 3.1 `docker-compose.yml` con `frontend`, `api` y `qdrant` (volumen persistente), healthchecks, `depends_on` con `service_healthy`, variables con valor por defecto y sondeo de archivos, más `.env.example` sin secretos; verificar con `docker compose config`.
- [x] 3.2 `Makefile` con `help`, `build`, `pull`, `up` (con `--wait`), `down`, `restart`, `ps`, `logs` y `check`, que ejecuta los checks dentro de los contenedores; verificar cada target.
- [x] 3.3 Verificar de extremo a extremo los escenarios de la spec:
  - `make up` deja los tres servicios sanos y la web muestra «API disponible»;
  - con `api` parada, la web muestra «no disponible»;
  - `make down` seguido de `make up` conserva el volumen de Qdrant;
  - sin `.env` arranca con los valores por defecto;
  - con otro `FRONTEND_PORT` en `.env`, la web sigue comunicándose con la API;
  - al guardar, la web y la API se recargan.

## 4. CI

- [ ] 4.1 Añadir a `ci.yml` los jobs `Frontend` (`npm ci`, `npm run check` y build) y `API` (`uv sync`, Ruff, mypy y pytest); verificar que pasan en el PR.

## 5. Documentación

- [x] 5.1 Registrar `docs/CONTRACTS/api.md` 0.1.0 con `GET /health` y añadirlo al índice de contratos.
- [x] 5.2 Actualizar ARCHITECTURE: §2 (fila de calidad con las herramientas elegidas), §3 y §4 (lo que pasa a Actual), §7 (comandos del Makefile) y §8 (herramientas y checks del CI).
- [x] 5.3 README: requisitos (Docker y GNU Make) y puesta en marcha con `make up`, con las URL de la web y de la API.
