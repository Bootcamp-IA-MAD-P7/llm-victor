## Context

En la web, `BriefingForm` hace `generatePost(...)` y entrega solo `res.text` a `App` mediante `onResult(text)`; `App` guarda ese texto y lo pasa a `ResultView`, que solo pinta el texto y la nota «Listo para revisar». La respuesta de la API ya incluye `provider` y `model` (`GenerateResponse` en `frontend/src/lib/api.ts`, backend en `backend/app/api/generate.py`) y el contrato `docs/CONTRACTS/api.md` ya los documenta en la salida de `POST /generate`. El punto de pérdida es la frontera web: `onResult` descarta esos campos. Ver proposal.md (Why).

## Goals / Non-Goals

**Goals:**

- Que el proveedor y el modelo devueltos por la API lleguen hasta la vista del resultado y se muestren junto al texto, con una etiqueta comprensible.
- Mantener la presentación informativa dentro de la sesión, sin tocar la petición, la generación ni el contrato.

**Non-Goals:**

- No cambiar la API ni el contrato (`provider` y `model` ya están en la respuesta).
- No implementar el fallback a OpenRouter (#18): el proveedor devuelto hoy es siempre `groq`; se muestra el valor efectivo que reporte la API.
- No persistir los metadatos entre sesiones (RNF-03) ni recuperarlos del catálogo `GET /models`.

## Decisions

- **`onResult` entrega el resultado completo de la generación, no solo el texto.** `BriefingForm` pasa el objeto `GenerateResponse` (`text`, `provider`, `model`) a `App`, que lo guarda y lo reenvía a `ResultView`. *Alternativas:* un callback aparte para los metadatos (dos actualizaciones de estado y más superficie); que `App` interprete la respuesta de la API (rompe la separación actual, donde el formulario posee la petición). Se opta por transportar el dato ya disponible.
- **El proveedor y el modelo se muestran en `ResultView`, en una línea de metadatos junto al texto**, con el estilo de texto secundario ya existente (`text-xs text-muted-foreground`), p. ej. «Generado con groq · llama-3.1-8b-instant». *Alternativas:* un componente propio (prematuro para una línea); mostrarlo en el formulario (el dato pertenece al resultado). Se mantiene la simplicidad ([PROJECT](../PROJECT.md) §5).
- **Se muestran los valores tal como los devuelve la API, sin etiquetas propias para el proveedor.** Los identificadores son estables y trazables (RNF-03) y todavía no existe un catálogo legible de proveedores (el catálogo de modelos es de modelos de texto). *Alternativa:* mapear `groq` a «Groq»; se descarta por inventar un dato que la API no publica.
- **Sin cambios en el contrato ni ADR.** La API y `docs/CONTRACTS/api.md` ya cubren `provider` y `model`; es una ampliación de presentación en la web, sin decisión técnica significativa. La versión del contrato (0.7.0) no cambia.

## Risks / Trade-offs

- [Hoy el proveedor devuelto es siempre `groq`; el valor deja de ser trivial cuando llegue el fallback #18] → La web pinta lo que devuelve la API, así que no habrá que rehacer la vista al añadir el fallback.
- [Identificadores de modelo largos pueden desbordar la línea] → Se usa una línea de texto pequeño y secundario coherente con la nota existente, que se ajusta al ancho del bloque de resultado.

## Open Questions

Ninguna que afecte a las specs, al enfoque o al desglose de tareas.
