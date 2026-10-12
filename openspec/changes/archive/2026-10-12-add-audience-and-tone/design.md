## Context

Ver `proposal.md` (Issue #12). Estado actual relevante:

- `backend/app/api/generate.py` define `GenerateRequest` con solo `brief` (validado no vacío) y `GenerateResponse` con `text`, `provider` y `model`.
- `backend/app/workflows/generate_direct.py` compone el prompt como `Genera una publicación de LinkedIn basada en este briefing:\n\n{brief}` y llama a `provider.generate_text`.
- `frontend/src/components/briefing-form.tsx` tiene un único `textarea` de briefing; `lib/api.ts` envía `{ brief }`.
- Contrato vigente: `docs/CONTRACTS/api.md` v0.2.0 (`POST /generate`). Requisitos: RF-02.

## Goals / Non-Goals

**Goals:**
- Elegir audiencia y tono antes de generar, con opciones acotadas y estables.
- Que los valores lleguen a la API, se validen y se reflejen en el prompt.
- Mantener el contrato y la documentación coherentes con la implementación.

**Non-Goals:**
- Contexto adicional (Issue #13), idioma (#14) y modelo (#16).
- Exponer un endpoint de opciones o validar en el navegador más allá de ofrecer valores válidos.
- Garantizar la calidad del resultado: igual que el briefing, el efecto se comprueba de forma razonable, no determinista.

## Decisions

1. **Valores permitidos con identificadores estables en inglés y etiquetas en español.** La API usa identificadores en inglés como valores del contrato; la web muestra etiquetas en español.

   - Audiencia (`audience`): `tech-professionals` → «Profesionales de tecnología», `ai-specialists` → «Especialistas en IA», `business-leaders` → «Líderes y directivos», `general-audience` → «Público general».
   - Tono (`tone`): `professional` → «Profesional», `friendly` → «Cercano», `inspiring` → «Inspirador», `educational` → «Divulgativo».

   Alternativa descartada: enviar las etiquetas en español; acopla el texto visible al contrato y complica traducirlo o renombrarlo.

2. **Validación con `Enum` de Pydantic.** `GenerateRequest` tipa `audience` y `tone` como enums con esos valores; un valor fuera del conjunto devuelve `422` y no ejecuta la generación. Alternativa descartada: validar a mano con `field_validator`; el enum es más declarativo y publica los valores en el esquema OpenAPI.

3. **Campos obligatorios con valor inicial en la web.** Los selectores arrancan en la primera opción (audiencia `tech-professionals`, tono `professional`) y siempre se envían, de modo que cada generación tiene audiencia y tono. Alternativa descartada: opcionales con valor por defecto en el backend; mantiene dos fuentes de verdad para el mismo comportamiento.

4. **El prompt incorpora audiencia y tono.** `generate_direct` recibe `audience` y `tone`, los traduce a su etiqueta y compone el prompt con una línea de audiencia y otra de tono antes del briefing. La traducción identificador → etiqueta vive en el backend, junto a los enums, para no depender del frontend. Alternativa descartada: enviar la etiqueta desde la web; expone texto de presentación en el contrato.

5. **El prompt no mezcla la configuración con el briefing.** La audiencia y el tono son instrucciones del sistema; el briefing se mantiene en un bloque aparte, alineado con el criterio de I1-E2 de no confundir contexto con instrucciones.

6. **Contrato: sube MINOR a `0.3.0`.** Se añaden campos a la solicitud de `POST /generate`; no se quitan ni renombran campos y la respuesta no cambia. La web y la API se despliegan juntas y comparten versión del contrato.

## Risks / Trade-offs

- [Risk] Deriva entre las opciones de la web y los enums de la API → Mitigación: ambos derivan del contrato documentado; un test de la API comprueba el conjunto permitido y un test de la web comprueba que el formulario los ofrece.
- [Risk] El cambio de forma de la solicitud rompe a un consumidor que no envíe los nuevos campos → Mitigación: hay un único consumidor (la web) que se actualiza en el mismo PR; se refleja como MINOR en el contrato.
- [Risk] El efecto de audiencia y tono en el texto no es determinista → Mitigación: se documenta como «en medida razonable», igual que el briefing; no se promete exactitud.

## Open Questions

Ninguna.
