## Why

La web solo sabe hablar con una API en `localhost`: si `VITE_API_URL` no está definida, `frontend/src/lib/api.ts` usa `http://localhost:8000` sin avisar, así que un build para un hosting quedaría apuntando a la máquina del usuario. Además, el `Dockerfile` de la web solo tiene la etapa de desarrollo: no existe una imagen que sirva los archivos estáticos compilados. [ADR-0001](/docs/ADR/0001-docker-first-deployable-services.md) exige que cada servicio se pueda desplegar por separado y que la web reciba la URL de la API por entorno.

Historia [#19](https://github.com/Glezino/ai-content-generator/issues/19), épica [#7](https://github.com/Glezino/ai-content-generator/issues/7) (I1-E6). Implementa RNF-05 y ADR-0001.

## What Changes

- La URL de la API se fija al compilar desde `VITE_API_URL`. Un build de producción sin ella, o con un valor que no sea una URL `http`/`https` absoluta, falla con un mensaje claro en lugar de quedar fijo a `localhost`.
- El valor por defecto `http://localhost:8000` se mantiene solo para el servidor de desarrollo y los tests, de modo que `make up` sigue funcionando sin configuración.
- El `Dockerfile` de la web gana una imagen de producción que compila la web con la URL recibida como argumento de build y sirve los estáticos, con fallback de rutas de la SPA.
- Nuevo comando del Makefile para construir esa imagen por separado, sin Compose.
- El CI construye la web con una URL de ejemplo y construye la imagen de producción.
- Se documentan en ARCHITECTURE las variables y la construcción de la imagen para un hosting futuro (Docker o hosting estático).
- **Fuera:** desplegar en un hosting y la configuración de la API para hosting (historia [#20](https://github.com/Glezino/ai-content-generator/issues/20)).

## Capabilities

### New Capabilities

- `deployable-services`: construcción de cada servicio para desplegarlo por separado y su configuración externa; empieza con la web (URL de la API al compilar e imagen propia).

### Modified Capabilities

Ninguna: el arranque local con valores por defecto (`local-environment`, «Configuración por entorno») no cambia.

## Impact

- **Web:** `src/lib/api.ts`, `src/env.d.ts`, `vite.config.ts` y el `Dockerfile` (nuevas etapas de build y producción); posible configuración del servidor estático.
- **Makefile y CI:** comando para la imagen de producción de la web; `VITE_API_URL` en el build del job `Frontend` y construcción de la imagen.
- **Documentación:** ARCHITECTURE §6, §7 y §9; comentario de `VITE_API_URL` en `.env.example`. README solo si cambia la puesta en marcha (no se prevé).
- **Contratos y ADR:** sin cambios; el cambio aplica ADR-0001 sin decisiones técnicas nuevas significativas.
- **Compose:** sin cambios; sigue usando la etapa de desarrollo.
