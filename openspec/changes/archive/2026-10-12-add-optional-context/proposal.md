## Why

Issue #13 (RF-02): el usuario debe poder aportar contexto adicional antes de generar y que la generación lo tenga en cuenta, sin que ese contexto se confunda con las instrucciones del sistema. Hoy `POST /generate` acepta `brief`, `audience` y `tone`, pero no un contexto libre, así que el usuario no puede matizar el resultado.

## What Changes

- Añadir un campo **opcional** de contexto al formulario de la web.
- Ampliar `POST /generate` con el campo opcional `context`; si falta o está vacío, la generación funciona igual que hoy.
- Incorporar el contexto al prompt de generación directa en un bloque de datos del usuario, separado de las instrucciones del sistema (audiencia, tono y consigna de generación).
- Documentar el campo `context` en `docs/CONTRACTS/api.md` (sube la versión MINOR, `0.3.0` → `0.4.0`).

## Capabilities

### New Capabilities
- (ninguna)

### Modified Capabilities
- `content-generation/direct-generation`: se añade el contexto opcional a la generación directa, su carácter opcional y su tratamiento como dato del usuario separado de las instrucciones del sistema.

## Impact

- `backend/app/api/generate.py`: campo opcional `context` en la solicitud, normalizado a ausente si está vacío.
- `backend/app/workflows/generate_direct.py`: el prompt incorpora el contexto como bloque de dato del usuario.
- `frontend/src/components/briefing-form.tsx` y `frontend/src/lib/api.ts`: campo de contexto opcional y su envío.
- `docs/CONTRACTS/api.md`: `POST /generate` con `context` (MINOR) y corrección del índice de contratos, que arrastra una versión desactualizada.
- Tests de API, de workflow y de componentes para los nuevos comportamientos.
