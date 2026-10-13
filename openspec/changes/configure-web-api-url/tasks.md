## 1. URL de la API al compilar

- [x] 1.1 Escribir primero los tests de la función pura que valida y normaliza `VITE_API_URL` (falta, vacía, relativa, esquema distinto de `http`/`https`, válida y barra final) e implementarla junto a `vite.config.ts`; verificar con `make check-frontend`.
- [x] 1.2 Usarla en `vite.config.ts`: error en `build` si la URL falta o no es válida, `http://localhost:8000` por defecto en `serve` y en los tests; quitar el fallback de `src/lib/api.ts` y declarar la variable como obligatoria en `src/env.d.ts`; verificar que `make check-frontend` pasa sin cambiar `api.test.ts`.
- [x] 1.3 Comprobar `npm run build` en el contenedor: falla sin `VITE_API_URL` nombrando la variable, falla con `/api` y, con `https://api.example.com`, el bundle contiene esa URL y no `localhost:8000`.
- [x] 1.4 Verificar que `make up` sin `.env` sigue mostrando la API disponible en la web.

## 2. Imagen de producción

- [x] 2.1 Añadir al `Dockerfile` las etapas `build` (`ARG VITE_API_URL`, `npm run build`) y `prod` (`nginxinc/nginx-unprivileged` alpine con versión fijada, `dist/` y `frontend/nginx.conf` con fallback de la SPA, puerto 8080), sin tocar `dev`; verificar que `docker build --target dev` sigue funcionando.
- [x] 2.2 Añadir `make image-frontend` (con su `.PHONY` y su línea en `make help`) que construye la imagen `prod` con `VITE_API_URL` sin Compose; verificar que falla sin la variable y que, con ella, la imagen arrancada responde la web en `/` y en una ruta inexistente.

## 3. CI

- [ ] 3.1 En el job `Frontend` de `.github/workflows/ci.yml`, definir `VITE_API_URL: https://api.example.com` para `npm run build` y añadir un paso que construya la imagen `prod`; verificar en el CI del PR.

## 4. Documentación

- [x] 4.1 Actualizar ARCHITECTURE §6 (URL obligatoria al compilar), §7 (`make image-frontend`) y §9 (construcción de la imagen, puerto 8080, `VITE_API_URL` como argumento de build en Docker y como variable de build en un hosting estático, fallback de la SPA), y el comentario de `VITE_API_URL` en `.env.example`; verificar que no queda ninguna referencia contradictoria.
