## Context

La generación directa ya transporta audiencia y tono desde el formulario hasta el prompt (historia #12) y contexto opcional (#13), con un contrato documentado en `docs/CONTRACTS/api.md`. Este cambio añade el idioma como una opción más de configuración, siguiendo exactamente el mismo patrón: enum en `workflows/generate_direct.py`, campo validado en `api/generate.py`, tipo y opciones en `frontend`, selector en `briefing-form.tsx` y delta de spec. Ver proposal.md (Why).

## Goals / Non-Goals

**Goals:**
- Llevar el idioma elegido desde la web hasta el prompt, con español por defecto en la web.
- Rechazar valores no válidos en la API sin ejecutar la generación.

**Non-Goals:**
- No traducir la interfaz (queda fuera del alcance de la historia #14).
- No cambiar el catálogo de modelos ni otros campos de configuración.

## Decisions

- **`language` obligatorio en la API, con `es` por defecto en la web.** Igual que `audience` y `tone`: la petición lo incluye siempre y la API valida el enum. Un valor ausente o fuera de los permitidos devuelve 422. *Alternativa:* dejar el campo opcional con default en el backend; se descarta por coherencia con el resto de la configuración y porque el único consumidor (el frontend) siempre lo envía.
- **Enum `Language` con valores `es`, `en`, `fr`, `it` y etiquetas en español para el prompt**, en el mismo archivo y con el mismo estilo que `Audience` y `Tone`. Se escribe en español («italiano») por consistencia con las etiquetas existentes de audiencia y tono.
- **El prompt incluye una línea `Idioma de salida: …`** antes del briefing, junto a audiencia y tono.
- **Sin ADR nuevo**: no hay decisión técnica significativa ni interfaz nueva; es un campo más del contrato existente.

## Risks / Trade-offs

- El prompt en español y con el idioma indicado como etiqueta puede no garantizar el idioma al 100 % con todos los modelos → la spec lo fija como «en medida razonable para esta versión», igual que audiencia y tono.
- Añadir un campo obligatorio rompería a un hipotético cliente que enviara peticiones sin `language` → no hay consumidores externos (pre-1.0) y el contrato sube a MINOR al ser un campo nuevo obligatorio para el único consumidor conocido.