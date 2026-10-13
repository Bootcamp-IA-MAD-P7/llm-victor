## Context

La API (FastAPI en `backend/app/`) expone hoy `/health` y `/generate` y configura los proveedores por entorno en `backend/app/config.py` con `Settings` (pydantic-settings). La web (`frontend/src/`) consulta la API mediante helpers tipados en `frontend/src/lib/api.ts` y presenta componentes por responsabilidad (`api-status.tsx`, `briefing-form.tsx`, `result-view.tsx`), con tests en Vitest. El contrato `frontend` → `api` está en `docs/CONTRACTS/api.md` (v0.5.0). Ver proposal.md (Why).

## Goals / Non-Goals

**Goals:**
- Publicar un endpoint de solo lectura con el catálogo de modelos configurados, identificadores estables, etiqueta legible y sin secretos.
- Que la web cargue el catálogo y muestre las opciones, con un mensaje comprensible si no puede cargarlo.
- Configurar el catálogo por entorno, con valores por defecto inocuos.

**Non-Goals:**
- No mostrar ni usar la selección del modelo en la generación: eso es la historia #16.
- No exponer claves, parámetros internos del proveedor ni detalles del fallback (I1-E5).
- No resolver todavía la relación entre `TEXT_MODELS` y `DEFAULT_MODEL_GROQ`.

## Decisions

- **Endpoint `GET /models` con respuesta `{"models": [{"id": …, "label": …}]}`.** El recurso es el modelo y la lista es su colección, acorde con `GET /health` y `POST /generate`. *Alternativas:* `GET /catalog` o `GET /models/catalog`; se descartan por ser menos RESTful y no aportar.
- **Formato de configuración `TEXT_MODELS` como pares `id|label` separados por comas.** Cada entrada tiene el identificador estable (usado como `id` público) y la etiqueta legible. Valor por defecto: el modelo por defecto actual de Groq con su etiqueta (`llama-3.1-8b-instant|Llama 3.1 8B Instant`). *Alternativas:* JSON en la variable, o derivar la etiqueta del id; se descartan por añadir formato o etiquetas poco legibles. El `id` coincide hoy con el nombre del modelo en Groq; es la pieza estable que la API devolverá y que #16 validará.
- **El catálogo se construye en `backend/app/catalog.py`** (modelo y parseo), y el endpoint vive en `backend/app/api/models.py`, registrado en `main.py` junto a los demás routers. Es responsabilidad del componente `api` «aplicar el catálogo de modelos» ([ARCHITECTURE §3](../ARCHITECTURE.md#3-componentes)).
- **El catálogo es configurado, no se obtiene dinámicamente de Groq.** El issue pide exponer «los modelos configurados»; además, la API de Groq no distingue los gratuitos y devolvería modelos de texto, audio y pago junto a detalles internos del proveedor, que habría que filtrar y reetiquetar igualmente. La lista configurada permite ofrecer solo los modelos gratuitos de texto que interesan, con ids estables y etiquetas legibles. *Alternativa:* consultar `GET /models` de Groq al vuelo; se descarta por lo anterior y porque añadiría una llamada externa a un endpoint que debe ser barato y estable.
- **La web consulta con un helper `fetchModels()` en `frontend/src/lib/api.ts`** y presenta la lista en un componente propio `model-catalog.tsx`, siguiendo el patrón de `api-status.tsx`. Muestra de solo lectura: la selección y el envío del modelo a `POST /generate` son de #16.
- **Contrato: versión 0.6.0 del API HTTP** (endpoint nuevo, compatible → MINOR). Se documenta en `docs/CONTRACTS/api.md` y se actualiza el índice.
- **Sin ADR nuevo**: es un endpoint de solo lectura dentro de la API existente, sin decisión técnica significativa ni interfaz externa.

## Risks / Trade-offs

- [El `id` coincide con el nombre del modelo en Groq: si el proveedor lo renombra, el id cambia y se rompe la estabilidad] → El `id` es el identificador público de producto; si en el futuro el catálogo mapea ids estables a modelos internos, el cambio queda confinado en la API sin tocar el contrato.
- [Un catálogo con un solo modelo por defecto hace la demostración trivial] → La lista se configura por entorno y el usuario puede añadir modelos con `TEXT_MODELS`; la elección de los modelos por defecto es decisión de producto (ver Open Questions).
- [Formato `id|label` propio] → Se documenta en `.env.example` y en el contrato; el parseo es simple y tipado.

## Open Questions

- ¿Qué modelos se publican por defecto en el catálogo? Hoy solo el modelo por defecto de Groq; se amplía por configuración sin cambiar el contrato.