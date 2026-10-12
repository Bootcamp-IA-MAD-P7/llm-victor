## Why

Issue #9: permitir al usuario generar una publicación de LinkedIn a partir de un briefing escrito, devolviendo un resultado revisable. Esto activa el flujo base de generación directa con Groq definido en arquitectura y establece el primer contrato funcional entre frontend y API para la generación.

## What Changes

- Añadir un endpoint `POST /generate` en la API para recibir un briefing y parámetros mínimos, y devolver el texto generado junto a metadatos (proveedor y modelo usados).
- Implementar un flujo de LangGraph de generación directa (`workflows/generate_direct`) que llama a Groq con el modelo seleccionado, respetando el diseño de fallback ya previsto (OpenRouter) aunque en esta historia solo se active por error/indisponibilidad según arquitectura.
- Registrar el contrato `frontend` → `api` para la generación en `docs/CONTRACTS/` (actualizar api.md a v0.2.0 con `/generate`).
- Añadir formulario de briefing en frontend y presentación del resultado (listo para revisar), sin publicar en LinkedIn.
- Configurar Groq en `providers` y leer la clave solo desde variables de entorno en el backend.

## Capabilities

### New Capabilities
- `content-generation/direct-generation`: generación directa desde briefing con parámetros mínimos (tema/instrucciones, idioma, modelo) devolviendo texto revisable y metadatos de proveedor/modelo.

### Modified Capabilities
- (ninguna) — no cambia requisitos existentes de specs; añade un nuevo endpoint/flujo coherente con RF-01, RF-03.

## Impact

- `backend/app/api/`: nueva ruta `/generate`
- `backend/app/workflows/`: nuevo flujo `generate_direct`
- `backend/app/providers/`: cliente Groq y lógica de generación
- `frontend/`: formulario de briefing + vista de resultado
- `docs/CONTRACTS/api.md`: añadir contrato `/generate` (versión MINOR)
- Configuración: `.env.example` (si procede añadir variables Groq) y compose
