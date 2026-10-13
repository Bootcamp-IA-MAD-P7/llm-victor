# Tareas — add-model-catalog

## 1. API y catálogo (backend)

- [x] 1.1 Definir el formato del catálogo: añadir `Settings.text_models` en `backend/app/config.py` (por defecto `llama-3.1-8b-instant|Llama 3.1 8B Instant`) y un módulo `backend/app/catalog.py` con `Model` (`id`, `label`) y su parseo (`id|label` separados por comas, etiqueta con respaldo al id); verificar que pasa el test de parseo (lista configurada, etiqueta por defecto y entrada malformada).
- [x] 1.2 Exponer el catálogo: endpoint `GET /models` en `backend/app/api/models.py` que devuelve `{"models": [...]}`, registrado en `backend/app/main.py`; verificar que pasa `backend/tests/test_models.py` (devuelve los modelos configurados con id y label y no incluye claves ni credenciales).

## 2. Frontend (web)

- [x] 2.1 Añadir el tipo `Model` (`id`, `label`) y `fetchModels()` en `frontend/src/lib/api.ts` (GET `/models`); verificar que pasan los tests de `api.test.ts`.
- [x] 2.2 Crear `frontend/src/components/model-catalog.tsx` que carga el catálogo y muestra las opciones con su etiqueta, con un mensaje si no puede cargarlo, e integrarlo en `App.tsx`; verificar que pasan los tests del componente y que se ven las opciones al arrancar la web.

## 3. Contrato y documentación

- [x] 3.1 Documentar `GET /models` en `docs/CONTRACTS/api.md` (sube a 0.6.0) y actualizar el índice en `docs/CONTRACTS/README.md`; verificar que el documento muestra el formato con id y label, sin secretos.
- [x] 3.2 Actualizar `.env.example` (variable `TEXT_MODELS` con valores inocuos) y el estado de los componentes `api` y `frontend` en `docs/ARCHITECTURE.md` §3; verificar que la documentación refleja el nuevo endpoint y el catálogo.

## 4. Verificación

- [x] 4.1 Sincronizar las specs (`openspec sync`), ejecutar `openspec validate`, los checks del proyecto (`make check`) y confirmar que las casillas de la historia #15 cubren formato del catálogo, exposición en la API y presentación en la web.