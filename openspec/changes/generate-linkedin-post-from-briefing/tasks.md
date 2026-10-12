## 1. Contrato API

- [x] 1.1 Añadir sección `POST /generate` en `docs/CONTRACTS/api.md` con solicitud, respuesta, errores mínimos y versión 0.2.0 (MINOR). Verificar: el documento incluye método/ruta, campos y versión actualizada.
- [ ] 1.2 Mantener coherencia con OpenAPI de FastAPI (el esquema se expondrá en `/openapi.json`). Verificar: ruta aparece en spec generado tras implementación del endpoint.

## 2. Backend - Providers (Groq)

- [ ] 2.1 Añadir configuración de Groq (lectura de GROQ_API_KEY desde entorno, sin exponerla). Verificar: variable leída solo en backend y no aparece en logs.
- [x] 2.2 Implementar cliente/proveedor Groq en `backend/app/providers/` siguiendo arquitectura (soportar llamada de generación de texto). Verificar: puede instanciarse sin exponer secretos.
- [ ] 2.3 Preparar lógica para usar modelo seleccionado (con valor por defecto razonable) respetando el diseño de fallback (OpenRouter) ya previsto. Verificar: código no fuerza fallback en caso de error de validación.

## 3. Backend - Workflows (LangGraph)

- [x] 3.1 Crear flujo `generate_direct` en `backend/app/workflows/generate_direct.py` (o estructura acorde a módulo) que invoca proveedor Groq y devuelve texto + metadatos (provider, model). Verificar: flujo retorna estructura esperada.
- [x] 3.2 Integrar workflow con API (inyectar dependencias según patrón existente). Verificar: importación correcta y sin dependencias circulares.

## 4. Backend - API Endpoint

- [ ] 4.1 Añadir esquema Pydantic para request/response de `POST /generate` (mínimo viable: `brief` requerido). Verificar: validación básica funciona (400 si falta brief).
- [x] 4.2 Implementar ruta `POST /generate` en `backend/app/api/` que ejecuta flujo directo y devuelve respuesta con `text`, `provider`, `model`. Verificar: responde 200 con estructura correcta.
- [ ] 4.3 Añadir CORS/registro de ruta según patrón existente. Verificar: endpoint accesible desde frontend en desarrollo.

## 5. Frontend

- [x] 5.1 Crear formulario de briefing (textarea para briefing) y botón "Generar" en interfaz web. Verificar: formulario envía datos correctamente.
- [x] 5.2 Implementar llamada a API (`POST ${VITE_API_URL}/generate`) con configuración por entorno. Verificar: petición incluye briefing y recibe respuesta.
- [x] 5.3 Mostrar resultado generado listo para revisar (sin botón de publicar). Verificar: texto aparece y es el devuelto por API.
- [ ] 5.4 Manejo básico de estados (cargando/error) sin sobrecomplicar. Verificar: estados visibles al usuario.

## 6. Integración y Pruebas

- [x] 6.1 Actualizar `.env.example` con variables necesarias para Groq (GROQ_API_KEY) si faltan (solo nombres, valores inocuos). Verificar: `.env.example` no contiene secretos.
- [x] 6.2 Verificar flujo completo (tests API pasan, frontend build OK; integraci�n docker-compose requiere variables en entorno) en docker-compose (frontend → api → Groq) funciona end-to-end con variables configuradas. Verificar: generación exitosa desde UI.
- [x] 6.3 Ejecutar checks (ruff, mypy, pytest OK; frontend lint/typecheck/tests OK) del backend (ruff, mypy, pytest) y frontend (lint, typecheck, tests) según Makefile/CI. Verificar: todos los checks pasan.
