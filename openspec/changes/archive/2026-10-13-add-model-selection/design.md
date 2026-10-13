## Context

La API (`backend/app/`) expone `GET /models` con el catálogo configurado (`TEXT_MODELS`, parseo en `backend/app/catalog.py`) y `POST /generate` con audiencia, tono, idioma y contexto (`backend/app/api/generate.py`). El proveedor `GroqProvider.generate_text(prompt, model)` ya acepta un modelo y, sin clave, devuelve un stub determinista. `generate_direct` ya transporta `model` hasta el proveedor, pero la API nunca lo recibe ni lo valida: siempre se usa el modelo por defecto. La web (`frontend/src/`) carga el catálogo en `model-catalog.tsx` (lista de solo lectura) y envía la generación desde `briefing-form.tsx` mediante `frontend/src/lib/api.ts`. Ver proposal.md (Why).

## Goals / Non-Goals

**Goals:**

- Que la petición de generación transporte un modelo del catálogo, que la API lo valide y que el proveedor genere con él.
- Ofrecer el selector de modelo en la web, con un modelo por defecto, y enviar el elegido.
- Comunicar de forma comprensible cuándo un modelo ya no está disponible, sin sustituirlo automáticamente, y permitir elegir otro.

**Non-Goals:**

- No implementar el fallback a OpenRouter ni la comparación de modelos (historias #18 y otras).
- No cambiar el catálogo ni su endpoint `GET /models`.
- No resolver la relación entre `TEXT_MODELS` y `DEFAULT_MODEL_GROQ` (pregunta abierta del catálogo).

## Decisions

- **`model` obligatorio en `POST /generate`, validado contra el catálogo configurado.** La API parsea `settings.text_models` y, si `model` no está entre los identificadores, responde 422 sin ejecutar la generación. *Alternativas:* campo opcional con modelo por defecto en el servidor (el usuario no elegiría y no se cumpliría RF-05); un `enum` en el esquema de la petición (no puede leer el catálogo configurado por entorno). Se opta por la validación explícita en la ruta, con acceso a `request.app.state.settings` como hace `GET /models`.
- **La web inicializa el selector con el primer modelo del catálogo** y deshabilita «Generar» si no hay ninguno cargado; así el campo obligatorio nunca se envía vacío por descuido. *Alternativa:* preseleccionar `DEFAULT_MODEL_GROQ`; se descarta porque el catálogo manda y puede no incluir ese id.
- **El selector vive en el formulario de generación (`briefing-form.tsx`), que carga el catálogo.** Sustituye a la lista de solo lectura de `model-catalog.tsx`: mostrar la misma lista y además un selector duplicaría la información y rompería la simplicidad ([PROJECT](../PROJECT.md) §5). El comportamiento del catálogo (mostrar las opciones con su etiqueta y comunicar si no se puede cargar) se mantiene, ahora desde el formulario, por lo que `content-generation/model-catalog` no cambia de requisitos. *Alternativa:* mantener la lista y añadir el selector aparte; se descarta por redundante.
- **Modelo no disponible = dos caminos, ambos sin fallback.** (a) Un modelo que ya no está en el catálogo se rechaza con 422 al validar. (b) Un modelo que sigue en el catálogo pero el proveedor rechaza como retirado/inexistente se traduce a un error propio. El proveedor (`providers/groq.py`, la pasarela del componente `api`) clasifica el error del SDK y lanza `ModelUnavailableError`; la API lo mapea a **409** con un mensaje genérico sin detalles internos. La web distingue el 409 y muestra un mensaje específico («el modelo ya no está disponible; elige otro»), refresca el catálogo y deja elegir otro conservando el briefing. *Alternativas:* devolver 500 (el usuario no sabría que debe cambiar de modelo); devolver 422 (lo confundiría con un valor no permitido y mezclaría ambos casos); recurrir a otro modelo (es el fallback de #18, fuera de alcance).
- **Clasificación del error por el proveedor, no por la API.** Detectar «modelo no disponible» exige conocer el SDK de Groq (código de estado 400/404 y marcas como `model_not_found`/`model_decommissioned`/`decommissioned`). Esa dependencia queda en `providers`, que informa del modelo efectivo y conoce los proveedores ([ARCHITECTURE §3](../ARCHITECTURE.md#3-componentes)); la API solo conoce la excepción de dominio. Sin clave (stub), un modelo del catálogo siempre se genera, así que la demostración de este camino usa un proveedor de prueba en los tests.
- **Contrato: versión 0.7.0 del API HTTP** (campo nuevo en la petición y código de error nuevo; compatible → MINOR), siguiendo el precedente del campo `language` en 0.5.0. Se documenta en `docs/CONTRACTS/api.md` y en el índice.
- **Sin ADR nuevo**: es un campo y un error dentro de la API existente, con el patrón ya establecido de validación y de catálogo configurado; no hay decisión técnica significativa ni interfaz externa nueva.

## Risks / Trade-offs

- [La clasificación del error del proveedor depende de cómo Groq informa del modelo retirado y podría no reconocer un caso] → Se reconoce por código de estado (400/404) más marcas textuales de modelo no encontrado/retirado; si no encaja, cae en el fallo genérico (500) sin romper nada ni inventar un falso positivo. Se afina con el proveedor real cuando haya clave.
- [La web del usuario puede tener un catálogo en caché y ofrecer un modelo ya retirado] → La API es la fuente de verdad: rechaza el modelo antiguo (422 si salió del catálogo, 409 si el proveedor lo rechaza) y la web, ante el 409, refresca el catálogo y permite reelegir.
- [Un catálogo con un solo modelo por defecto hace la elección trivial] → La elección real depende de configurar más modelos en `TEXT_MODELS`; es la misma pregunta abierta que en #15 y no cambia el contrato ni este diseño.

## Open Questions

Ninguna que afecte a las specs, al enfoque o al desglose de tareas.
