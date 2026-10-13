# Design

## Context

Hoy `generate_direct` (`backend/app/workflows/generate_direct.py`) llama directamente a `GroqProvider` (`backend/app/providers/groq.py`), que lanza `ModelUnavailableError` cuando el modelo está retirado y propaga el resto de fallos. `POST /generate` (`backend/app/api/generate.py`) los traduce a `409` o `500`. ARCHITECTURE §5 ya prevé Groq con fallback a OpenRouter y ARCHITECTURE §52 sitúa la pasarela de modelos en `providers`. `Settings` ya tiene `openrouter_api_key`; `.env.example` ya declara `OPENROUTER_API_KEY`. Ver proposal.md - Why.

## Goals / Non-Goals

**Goals:**

- Encapsular en la capa `providers` el intento con Groq y el fallback a OpenRouter, para que el flujo de generación no conozca a los proveedores concretos.
- Clasificar los fallos de forma que solo los elegibles disparen el fallback.
- Devolver el proveedor y el modelo efectivos sin cambios en la web.

**Non-Goals:**

- No mapear cada modelo del catálogo a su equivalente en OpenRouter: el fallback usa un único `OPENROUTER_MODEL` configurable.
- No cambiar el comportamiento de modelo no disponible (`409`) ni el de validación (`422`).
- No añadir imagen, pago, reintentos múltiples ni persistencia de metadatos.

## Decisions

- **Pasarela en `providers/` (`TextProviderGateway`).** Envuelve un proveedor primario (Groq) y uno alternativo (OpenRouter) y expone el mismo `generate_text(prompt, model) -> dict`. El flujo de generación recibe la pasarela como `provider`. *Alternativas:* poner el fallback en el workflow (mezcla persistencia de proveedores con el flujo LangGraph) o en el endpoint (acopla el HTTP a la política de fallback). Se sigue ARCHITECTURE §52.
- **Fallback solo ante fallos elegibles, clasificados por estado HTTP.** Elegible si el error no tiene estado (conexión o *timeout*, es decir, Groq inaccesible), o si el estado es `429` (límite o *rate limit*) o `≥ 500` (fallo del proveedor). No elegible: `4xx` (validación, autenticación) y `ModelUnavailableError`, que se propaga tal cual. *Alternativas:* recurrir a OpenRouter ante cualquier excepción (dispararía el fallback ante errores de la propia solicitud). Se alinea con los criterios de aceptación de #18 y con «Comunicar un modelo no disponible» de RF-05.
- **Un único `OPENROUTER_MODEL` configurable por entorno** (por defecto `meta-llama/llama-3.1-8b-instruct`). El fallback puede cambiar de modelo y la respuesta informa el efectivo. *Alternativa:* un mapa modelo→modelo (más configuración y mantenimiento); descartado por KISS para el POC (decisión de producto confirmada).
- **Cliente de OpenRouter con `httpx` sobre su API compatible con OpenAI** (`POST {base_url}/chat/completions`). Sin clave, devuelve un *stub* determinista, igual que `GroqProvider`, para desarrollo y tests sin red. Se añade `httpx` como dependencia directa (hoy llega de forma transitiva a través del SDK de Groq). *Alternativas:* el SDK `openai` como dependencia nueva (más peso para una sola llamada). *Nota:* los detalles del formato de la petición pertenecen a tasks/implementación, no a la spec.
- **La API construye la pasarela desde `Settings`** y la pasa a `generate_direct`; el workflow conserva su parámetro `provider` (duck typing sobre `generate_text`), de modo que los tests existentes que inyectan un proveedor falso siguen valiendo. El `409` por modelo no disponible y el `422` de validación no cambian.
- **Contrato `docs/CONTRACTS/api.md` a 0.8.0 (MINOR).** La interfaz no cambia; se amplían los valores posibles de `provider` (`groq`, `openrouter`) y se documenta el fallback. Sin ADR: implementa una dirección ya aceptada en ARCHITECTURE §5.

## Risks / Trade-offs

- [`httpx` como dependencia transitiva frágil] → Se declara explícitamente en `backend/pyproject.toml`.
- [Un proveedor alternativo distinto puede dar un modelo/calidad diferentes] → El modelo alternativo es configurable y la respuesta siempre informa del proveedor y modelo efectivos (RNF-03).
- [Filtrar detalles o secretos en el error de OpenRouter] → La pasarela no adjunta el cuerpo de la respuesta; el endpoint mantiene el mensaje genérico `Generation failed` que ya usa.
- [Solo un intento de fallback: un fallo de OpenRouter no se reintenta] → Suficiente para el POC; si ambos fallan, se comunica el error comprensible (RNF-07).
- [Sin clave de OpenRouter, el fallback devuelve el *stub*] → Comportamiento de desarrollo coherente con Groq; en producción la clave se aporta por entorno.

## Open Questions

Ninguna que afecte a las specs, al enfoque o al desglose de tareas.
