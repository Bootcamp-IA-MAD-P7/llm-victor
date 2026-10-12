## Context

Ver `proposal.md` (Issue #10). Estado actual relevante:

- `backend/app/api/generate.py` usa Pydantic con `brief: str = Field(..., min_length=1)`, que rechaza la cadena vacía pero acepta solo espacios y devuelve `422` (no el `400` que documenta hoy `docs/CONTRACTS/api.md`). La generación se envuelve en `try/except` y devuelve `500` con detalle genérico.
- `backend/app/providers/groq.py` captura cualquier excepción de la llamada real y devuelve un texto `[FALLBACK-STUB]`, de modo que un fallo del proveedor no llega a la API como error.
- `frontend/src/components/briefing-form.tsx` descarta en silencio el envío si `brief.trim()` está vacío; `lib/api.ts` lanza un `Error` genérico ante cualquier respuesta no `ok`; `App.tsx` muestra "Cargando..." y "Error al generar el contenido.".

Contrato vigente: `docs/CONTRACTS/api.md` v0.2.0 (`POST /generate`). Requisitos: RF-01, RNF-07.

## Goals / Non-Goals

**Goals:**
- Rechazar el briefing vacío o en blanco de forma consistente en la web y en la API.
- Estado de carga visible y errores comprensibles que distingan causa, conservando el briefing.
- Contrato de error de `POST /generate` documentado y coherente con la implementación.

**Non-Goals:**
- Fallback de proveedor (OpenRouter) y cambios de forma del contrato de generación.
- Audiencia, tono, idioma o modelo (otras historias de I1-E1).

## Decisions

1. **Validación en la web y en la API (defensa en profundidad).** La web valida `brief.trim()` y no llama a la API si está vacío; la API lo valida de nuevo. Alternativa: validar solo en un lado; se descarta porque RF-01 exige que ambas rechacen el briefing vacío.

2. **Normalizar y rechazar el briefing en blanco en la API.** Un validador de Pydantic hace `strip()` y rechaza el resultado vacío, de modo que `""`, `"   "` y ausente se comportan igual. El texto almacenado es el ya recortado.

3. **Código de error: `422` para validación y `500` para fallo de generación.** Se usa el `422` de Pydantic/FastAPI (idiomático) y se documenta; el contrato decía `400`, que era inexacto. Alternativa: forzar `400` con un manejador de excepciones; se descarta por añadir código para no ganar nada observable. No cambian endpoints ni campos, así que la versión del contrato se mantiene en `0.2.0` completando su sección de errores.

4. **El proveedor propaga los fallos reales.** Se elimina el `except` que convertía un fallo de Groq en texto `[FALLBACK-STUB]`; el stub se conserva solo cuando no hay `GROQ_API_KEY` (desarrollo y tests). Alternativa: dejar el enmascarado; se descarta porque sin propagación la API nunca devuelve `500` y RNF-07 no se cumple en la práctica. Esto lo aprueba la persona en la Parada 2.

5. **Errores tipados en el frontend.** `lib/api.ts` lanza un `ApiError` con el `status`; la interfaz traduce a mensajes en español: uno para fallo de conexión/API no disponible (red o timeout) y otro para fallo de generación (`5xx`), sin mostrar detalles internos.

6. **Conservar el briefing.** El estado de la vista (`idle | loading | done | error`) vive en `App` y el texto del briefing vive en `BriefingForm`, que permanece montado: el comentario del usuario no se pierde ni al fallar ni al reintentar. El botón se deshabilita mientras `loading`.

7. **Contrato de error.** `docs/CONTRACTS/api.md` documenta en `POST /generate` los códigos `422` (briefing ausente/vacío/en blanco) y `500` (fallo de generación), con qué debe hacer el consumidor.

## Risks / Trade-offs

- [Risk] Quitar el enmascarado del proveedor altera un comportamiento aprobado en #9 → Mitigación: es necesario para que un fallo sea observable; se presenta en la Parada 2 y se conserva el stub sin clave.
- [Risk] Corregir el contrato de `400` a `422` es un cambio sobre un documento aceptado → Mitigación: no cambia endpoints ni campos; se documenta y se avisa en la revisión.
- [Risk] El `500` es difícil de provocar con el stub en tests → Mitigación: en el test de la API se mockea el workflow para que lance una excepción.

## Open Questions

Ninguna.
