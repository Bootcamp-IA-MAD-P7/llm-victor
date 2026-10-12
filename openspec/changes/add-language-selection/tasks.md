# Tareas — add-language-selection

## 1. API (backend)

- [x] 1.1 Añadir el enumerado `Language` (`es`, `en`, `fr`, `it`) y `LANGUAGE_LABELS` en `app/workflows/generate_direct.py`, y que el prompt incluya una línea `Idioma de salida: …`; verificar que el test del prompt con idioma pasa (cubre las cuatro etiquetas).
- [x] 1.2 Añadir el campo obligatorio `language` a `GenerateRequest` y pasarlo a `generate_direct`; verificar que `pytest backend/tests/test_generate.py` pasa, con casos para los cuatro idiomas válidos y el rechazo de uno no válido sin ejecutar la generación.

## 2. Frontend

- [x] 2.1 Añadir el tipo `Language` y el campo `language` en `app` en `frontend/src/lib/api.ts` (interfaces y petición); verificar que pasan los tests de `api.test.ts`.
- [x] 2.2 Añadir `LANGUAGE_OPTIONS` y `DEFAULT_LANGUAGE = 'es'` en `frontend/src/lib/generation-options.ts` y el selector de idioma en `briefing-form.tsx`, enviándolo en la petición; verificar que pasan los tests de `briefing-form.test.tsx` y que el formulario ofrece las cuatro opciones con español por defecto.

## 3. Contrato y documentación

- [ ] 3.1 Actualizar `docs/CONTRACTS/api.md` (campo `language` en `POST /generate` y versión 0.5.0) y el índice en `docs/CONTRACTS/README.md` si procede; verificar que el documento muestra los cuatro valores permitidos y el error 422.

## 4. Verificación

- [x] 4.1 Sincronizar las specs (`openspec sync`), ejecutar `openspec validate`, los checks del proyecto (`make check`) y confirmar que las casillas de la historia #14 cubren selector, contrato/prompt y verificación de los cuatro idiomas y del rechazo.