## Context

Ver [proposal.md](proposal.md) — Why. El estado actual y las restricciones que condicionan el enfoque:

- `frontend/src/lib/api.ts` resuelve `API_URL` con `import.meta.env.VITE_API_URL ?? 'http://localhost:8000'`; `src/env.d.ts` declara la variable como opcional y `api.test.ts` espera `http://localhost:8000`.
- `frontend/Dockerfile` solo tiene las etapas `base` y `dev` (servidor de Vite). `.dockerignore` ya excluye `node_modules` y `dist`.
- `docker-compose.yml` construye la web con `target: dev` e inyecta `VITE_API_URL` calculada desde `API_PORT`.
- El job `Frontend` del CI ejecuta `npm run check` y `npm run build` sin `VITE_API_URL`.
- [ARCHITECTURE §9](/docs/ARCHITECTURE.md#9-despliegue) prevé Railway (imagen Docker por servicio) o Vercel (build estático con `npm run build`): la validación de la URL no puede vivir solo en el Dockerfile.
- No hace falta Node en el equipo: todo comando local va por Docker.

## Goals / Non-Goals

**Goals:**

- Que ningún build de producción apunte a `localhost` por omisión, sea con Docker o con un hosting estático.
- Una imagen de producción de la web pequeña, sin Node en runtime y que no se ejecute como root.

**Non-Goals:**

- Cambiar la URL sin recompilar (configuración en runtime): las variables de Vite se fijan al compilar, como ya dice ARCHITECTURE §6.
- Publicar la imagen en un registro, desplegarla o cambiar Compose.
- La configuración de la API para hosting (CORS, puerto): historia [#20](https://github.com/Glezino/ai-content-generator/issues/20).

## Decisions

### 1. Validar la URL en `vite.config.ts`

`vite.config.ts` lee `VITE_API_URL` con `loadEnv`. En `vite build` exige que exista y que sea una URL `http`/`https` absoluta; si no, lanza un error que nombra la variable. En `serve` y en los tests, si falta, inyecta `http://localhost:8000`. El valor se normaliza sin barra final antes de exponerlo a la app. `api.ts` deja de tener fallback y `env.d.ts` declara la variable como obligatoria.

*Alternativas:* validar solo en el Dockerfile (no cubre Vercel ni `npm run build` del CI); validar en runtime en `api.ts` (el error llegaría al usuario en lugar de al build).

Se exige una URL absoluta y no se admiten rutas relativas (`/api`) porque web y API se despliegan como servicios separados con su propio dominio; si un proxy inverso lo necesitara, se reabriría.

### 2. Etapas `build` y `prod` en el mismo Dockerfile

- `build` (desde `base`): `ARG VITE_API_URL`, `npm ci`, copia del código y `npm run build`. La validación de la decisión 1 hace fallar la imagen si falta el argumento.
- `prod`: imagen `nginxinc/nginx-unprivileged` (alpine, versión fijada) con `dist/` y una configuración mínima (`try_files $uri /index.html`) en `frontend/nginx.conf`. Escucha en el puerto 8080, sin root.

`dev` no cambia y Compose sigue usando `target: dev`. Al ser la última etapa, `prod` es lo que se construye si no se indica `--target`, que es lo que hacen por defecto las plataformas.

*Alternativas:* `vite preview` (no está pensado para producción y deja Node en runtime); `serve` u otro servidor de Node (imagen mayor y una dependencia más). Railway acepta imágenes con nginx sin configuración extra; Railway pasa las variables del servicio como `ARG` declarados.

### 3. Comando `image-frontend` en el Makefile

`make image-frontend VITE_API_URL=https://…` ejecuta `docker build --target prod --build-arg VITE_API_URL=… -t ai-content-studio-frontend:prod frontend`, sin Compose. Si falta `VITE_API_URL`, el build falla por la decisión 1. Se nombra `image-` para no confundirlo con `build-frontend`, que construye la imagen de desarrollo de Compose.

*Alternativa:* documentar solo el `docker build`. Se descarta porque el Makefile es la fuente de verdad de los comandos (ARCHITECTURE §7).

### 4. CI

El job `Frontend` define `VITE_API_URL: https://api.example.com` para `npm run build`, y un paso nuevo construye la imagen `prod` con `docker build` (sin publicarla), para que un fallo del Dockerfile se vea en el PR.

### 5. Tests

- `api.test.ts` sigue esperando `http://localhost:8000`: en los tests la URL la inyecta `vite.config.ts`, así que el test cubre que la app usa la URL configurada.
- La validación de la URL se extrae a una función pura junto a `vite.config.ts` (TDD: falta, vacía, relativa, otro esquema, válida y barra final).
- El build y la imagen se comprueban a mano y en el CI: con y sin `VITE_API_URL`, y que la imagen sirve `/` y una ruta inexistente.

## Risks / Trade-offs

- [Cambiar la API exige recompilar la web] → Aceptado y documentado en ARCHITECTURE §6 y §9; la configuración en runtime queda fuera.
- [El puerto 8080 de la imagen difiere del 5173 de desarrollo] → Se documenta en ARCHITECTURE §9; las plataformas exponen el puerto que indica la imagen o una variable.
- [Un build local con `npm run build` sin variable ahora falla] → Es el comportamiento buscado; el mensaje indica cómo definirla.

## Migration Plan

Sin migración: el entorno local no cambia y no hay despliegues. Revertir es volver al Dockerfile y al fallback anteriores.
