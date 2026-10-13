# Tareas — show-provider-and-model

## 1. Web: transportar y mostrar el proveedor y el modelo

- [x] 1.1 Cambiar `onResult` en `frontend/src/components/briefing-form.tsx` para entregar el resultado completo de `generatePost` (`text`, `provider`, `model`) en lugar de solo el texto, y adaptar `frontend/src/App.tsx` para conservarlos y pasarlos a `ResultView`; verificar con `frontend/src/App.test.tsx` que, tras generar, el proveedor y el modelo devueltos por la API llegan a la vista del resultado.
- [x] 1.2 Mostrar el proveedor y el modelo en `frontend/src/components/result-view.tsx` junto al texto, en una línea secundaria comprensible (p. ej. «Generado con groq · llama-3.1-8b-instant»); verificar con test que la vista los presenta cuando hay resultado y no los muestra sin él.

## 2. Verificación

- [x] 2.1 Sincronizar las specs (`openspec sync`), ejecutar `openspec validate` y los checks del proyecto (`make check`), y confirmar que las casillas de la historia #17 (respuesta con proveedor y modelo efectivos, y su presentación junto al resultado) quedan cubiertas.

## Workflow follow-up

- Archivar el cambio tras aprobar la revisión del PR.
- Verificar el resultado archivado.
