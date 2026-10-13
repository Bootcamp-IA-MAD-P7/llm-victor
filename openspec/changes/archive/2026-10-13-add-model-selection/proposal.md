## Why

La historia #16 requiere que la generación use el modelo que elige el usuario (RF-05). Hoy la API publica el catálogo (`GET /models`) pero la generación ignora esa elección y siempre usa el modelo por defecto, así que el usuario no puede elegir ni se rechaza un modelo fuera del catálogo.

## What Changes

- La petición `POST /generate` acepta un campo `model` obligatorio: el identificador elegido del catálogo. La API lo valida contra el catálogo configurado y rechaza con un error de validación (4xx) un modelo que no está en él, sin ejecutar la generación.
- El modelo elegido se pasa al flujo y al proveedor, que genera con él; la respuesta informa del modelo efectivo usado.
- El frontend ofrece un selector de modelo con las opciones del catálogo (primer modelo por defecto) en el formulario de generación, y envía el elegido.
- Si el modelo deja de estar disponible, el sistema lo comunica y permite elegir otro: un modelo que ya no está en el catálogo se rechaza en la API (4xx) y un modelo que el proveedor rechaza como no disponible se comunica con un error propio (409). En ningún caso se sustituye el modelo automáticamente.
- El contrato `docs/CONTRACTS/api.md` documenta el campo `model` y el nuevo error (sube a 0.7.0).

## Capabilities

### New Capabilities

Ninguna.

### Modified Capabilities

- `content-generation/direct-generation`: la generación acepta y aplica el modelo elegido del catálogo, lo valida y comunica cuándo deja de estar disponible, sin generar varias respuestas ni comparar modelos.

## Impact

- `docs/CONTRACTS/api.md` y `docs/CONTRACTS/README.md`: campo `model` en `POST /generate` y error 409 (versión 0.7.0).
- `backend/app/api/generate.py`: campo `model` en la petición, validación contra el catálogo y mapeo del modelo no disponible.
- `backend/app/providers/groq.py`: uso del modelo elegido y clasificación del error de modelo no disponible.
- `backend/app/workflows/generate_direct.py`: paso del modelo (ya soportado) al proveedor.
- `backend/tests/test_generate.py`: validación, uso del modelo y modelo no disponible.
- `frontend/src/lib/api.ts`: campo `model`, envío y mensaje del error de modelo no disponible.
- `frontend/src/components/briefing-form.tsx` y `frontend/src/App.tsx`: selector de modelo; `frontend/src/components/model-catalog.tsx` deja de ser una lista de solo lectura.
- `openspec/specs/content-generation/direct-generation/spec.md`: requisito delta sincronizado al publicar.
