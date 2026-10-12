## Why

El proyecto aún no tiene código. Antes de construir capacidades de producto, el walking skeleton necesita una base ejecutable en la que web, API y Qdrant arranquen juntos con un comando, se comuniquen y pasen checks de calidad en el CI, para validar la arquitectura Docker-first ([ADR-0001](/docs/ADR/0001-docker-first-deployable-services.md)) desde el primer incremento.

Historia [#8](https://github.com/Glezino/ai-content-generator/issues/8), épica [#2](https://github.com/Glezino/ai-content-generator/issues/2) (I1-E1). No implementa ningún RF directamente: es la base técnica que habilita RF-01.

## What Changes

- `frontend/`: aplicación React + Vite + TypeScript con Tailwind CSS y shadcn/ui, cuya página inicial muestra si la API está disponible.
- `backend/`: servicio `api` con FastAPI y un endpoint de salud.
- Dockerfile con comprobación de salud para cada servicio de aplicación, y `docker-compose.yml` con `frontend`, `api` y `qdrant`, este con volumen persistente.
- Configuración por entorno (puertos, URL de la API, orígenes CORS y URL de Qdrant), con `.env.example` sin secretos.
- `Makefile` con comandos globales para el ciclo de vida del conjunto y para ejecutar los checks.
- Herramientas de test, lint, formato y tipos de `frontend` y `api`, y sus checks en el CI.

## Capabilities

### New Capabilities

- `local-environment`: arranque y operación del sistema en local con Docker Compose y Makefile, salud de los servicios y estado de la API visible en la web.

### Modified Capabilities

Ninguna.

## Impact

- **Código nuevo:** `frontend/`, `backend/`, `docker-compose.yml`, `Makefile`, `.env.example`.
- **CI:** `.github/workflows/ci.yml` gana los jobs de `frontend` y `api`.
- **Dependencias:** Node.js y npm para la web; Python y uv para la API; imágenes de Docker de Node, Python y Qdrant.
- **Documentación:** README (puesta en marcha); ARCHITECTURE §2 (stack de calidad), §3 y §4 (componentes y estructura que pasan a Actual), §7 (comandos) y §8 (calidad y CI). No hay contratos estables todavía: el de generación llega en #9.
- **Fuera:** generación de contenido (#9), errores de generación (#10), comandos por servicio y consola (#11) y preparación para el despliegue (I1-E6).
