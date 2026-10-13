# Tareas — add-model-selection

## 1. API: validar y usar el modelo

- [x] 1.1 Añadir `model: str` a `GenerateRequest` en `backend/app/api/generate.py` y rechazar con 422 si falta o no está en el catálogo (`parse_catalog(Settings.text_models)`), sin ejecutar la generación; verificar con tests de API que un modelo del catálogo se acepta y que un modelo ausente o fuera del catálogo se rechaza sin llamar al flujo.
- [x] 1.2 Pasar el `model` recibido a `generate_direct` y confirmar que el proveedor lo usa y que la respuesta informa del modelo efectivo; verificar con un proveedor de prueba que captura el modelo solicitado.
- [x] 1.3 Clasificar como `ModelUnavailableError` el error del proveedor cuando el modelo deja de estar disponible y mapearlo a 409 en `generate.py` con un mensaje sin detalles internos; verificar con tests que un modelo rechazado por el proveedor responde 409 (no 500) y que no se filtra el detalle.

## 2. Frontend: selector de modelo

- [x] 2.1 Añadir `model` a `GenerateRequest` y enviarlo en `generatePost`, y mapear el 409 a un mensaje específico en `generationErrorMessage`; verificar con tests de `api.test.ts` que el modelo se envía y que el 409 explica que el modelo ya no está disponible.
- [x] 2.2 Cargar el catálogo y ofrecer un selector de modelo en `briefing-form.tsx` (primer modelo por defecto, mensaje si no carga, «Generar» deshabilitado sin modelo), retirar la lista de `model-catalog.tsx` y su uso en `App.tsx`; verificar con tests del formulario que se ven las opciones, hay modelo por defecto, se envía el elegido y se comunica si el catálogo no carga.
- [x] 2.3 Ante un error de modelo no disponible, refrescar el catálogo y permitir elegir otro conservando el briefing; verificar con test que tras el 409 se recargan los modelos y el briefing sigue en el formulario.

## 3. Contrato y documentación

- [x] 3.1 Documentar el campo `model` (obligatorio) y el error 409 en `docs/CONTRACTS/api.md` (sube a 0.7.0) y actualizar el índice en `docs/CONTRACTS/README.md`; verificar que el documento describe el campo, el rechazo de un modelo fuera del catálogo y el error de modelo no disponible.

## 4. Verificación

- [x] 4.1 Sincronizar las specs (`openspec sync`), ejecutar `openspec validate` y los checks del proyecto (`make check`), y confirmar que las casillas de la historia #16 cubren el selector, la validación y uso del modelo y el aviso de modelo no disponible.
