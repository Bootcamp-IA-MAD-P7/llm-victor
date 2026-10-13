## Why

La historia #17 requiere que el usuario vea qué proveedor y qué modelo produjeron el texto (RNF-03). La API ya devuelve `provider` y `model` en la respuesta de `POST /generate`, pero la web descarta esos metadatos y solo muestra el texto, así que el usuario no sabe con qué configuración se generó.

## What Changes

- La web conserva el `provider` y el `model` de la respuesta de generación y los muestra junto al resultado, con una etiqueta comprensible.
- La presentación es solo informativa dentro de la sesión: no cambia la petición, ni la generación, ni persiste los metadatos entre sesiones.
- El contrato `docs/CONTRACTS/api.md` ya documenta `provider` y `model` en la salida de `POST /generate`; no cambia de versión.

## Capabilities

### New Capabilities

Ninguna.

### Modified Capabilities

- `content-generation/direct-generation`: además de devolver el proveedor y el modelo efectivos en la respuesta, la web los muestra junto al resultado.

## Impact

- `frontend/src/lib/api.ts`: `onResult`/consumo conservan `provider` y `model` de `GenerateResponse` (la interfaz ya los declara).
- `frontend/src/components/briefing-form.tsx`: `onResult` entrega el resultado completo (o su `text`, `provider` y `model`) en lugar de solo el texto.
- `frontend/src/App.tsx`: conserva y propaga el proveedor y el modelo al resultado.
- `frontend/src/components/result-view.tsx`: muestra el proveedor y el modelo junto al texto.
- `frontend/src/App.test.tsx` (y/o un test del resultado): verificar que se muestran el proveedor y el modelo.
- `openspec/specs/content-generation/direct-generation/spec.md`: requisito delta sincronizado al publicar.
- Sin cambios en la API ni en el contrato; sin ADR (presentación informativa, sin decisión técnica significativa).
