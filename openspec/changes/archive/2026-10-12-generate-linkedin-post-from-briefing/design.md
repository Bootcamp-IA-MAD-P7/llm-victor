## Context

Issue #9: generar una publicación de LinkedIn desde un briefing con Groq. Arquitectura actual define flujo directo en §5 con fallback a OpenRouter, contrato API v0.1.0 en `docs/CONTRACTS/api.md`, componentes `frontend`, `api`, `workflows`, `providers`, `knowledge`, `evaluation`. Backend FastAPI, LangGraph para workflows, frontend Vite, perfil en localStorage, API sin estado persistente.

## Goals / Non-Goals

**Goals:**
- Implementar flujo directo de generación con Groq siguiendo arquitectura §5.
- Añadir endpoint `POST /generate` en API y registrarlo en contrato (v0.2.0 MINOR).
- Formulario de briefing + presentación de resultado en frontend (solo revisión, sin publicar).
- Asegurar que clave Groq solo está en backend.

**Non-Goals:**
- Validaciones detalladas, manejo avanzado de errores, audiencia/tono/idioma complejos (fuera de alcance de #9).
- RAG/Graph RAG, imagen, evaluación avanzada, multiusuario (más adelante).
- Fallback automático a OpenRouter en esta historia (se mantiene lógica prevista pero no es requisito explícito de AC; se deja preparado).

## Decisions

1. **Endpoint path**: usar `POST /generate` (simple, alineado con arquitectura que menciona endpoint de generación). Alternativas: `/posts/generate` (más RESTful pero añade anidamiento). Decisión: `/generate` por simplicidad y coherencia con naming previsto.

2. **Esquema de request/response**: mínimo viable alineado con AC. Request: `{ brief: string, language?: string, audience?: string, tone?: string, model?: string, use_profile?: bool }`? Pero AC dice "sin validaciones detalladas, audiencia/tono/idioma y modelo fuera de alcance" en versión básica - nos ajustamos a contrato mínimo: pedir briefing y devolver texto + metadatos. Decisión: campos mínimos `{ brief: string }` con respuesta `{ text: string, provider: string, model: string }`. Dejar campos opcionales comentados en contrato para evolución.

3. **Workflow con LangGraph**: crear `workflows/generate_direct.py` con nodo simple (invoke LLM Groq) siguiendo patrón modular (`workflows/` separado de `providers/`). Decisión: mantener separación providers/workflows según arquitectura.

4. **Proveedor Groq**: añadir cliente en `providers/groq.py` o en módulo de providers siguiendo estructura. Arquitectura indica `providers` pasa a Groq/OpenRouter. Decisión: seguir diseño existente (agregar implementación concreta de Groq).

5. **Contrato**: actualizar `docs/CONTRACTS/api.md` añadiendo sección `/generate` (versión 0.2.0 MINOR). Artefacto ejecutable OpenAPI se publica en `/openapi.json` (ya existe en FastAPI); documento .md sigue siendo fuente de verdad con enlace.

6. **Frontend**: formulario simple (textarea para briefing, botón generar) que llama a `VITE_API_URL/generate`. Mostrar resultado listo para revisar (texto plano). Sin publicación.

## Risks / Trade-offs

- [Risk] Cambiar contrato API rompe frontend si no sincronizado → Mitigación: actualizar frontend y API en misma historia/PR.
- [Risk] Dependencia externa Groq sin mock para tests → Mitigación: mantener tests existentes, añadir tests del endpoint con mocking si procede, siguiendo pytest + FastAPI TestClient.
- [Risk] Configuración env (GROQ_API_KEY) ausente → Mitigación: leer desde backend, documentar en `.env.example`, fallar con error claro pero sin exponer secreto.
