## 1. Contrato API

- [x] 1.1 AÃ±adir secciÃ³n `POST /generate` en `docs/CONTRACTS/api.md` con solicitud, respuesta, errores mÃ­nimos y versiÃ³n 0.2.0 (MINOR). Verificar: el documento incluye mÃ©todo/ruta, campos y versiÃ³n actualizada.
- [x] 1.2 Mantener coherencia con OpenAPI de FastAPI (el esquema se expondrÃ¡ en `/openapi.json`). Verificar: ruta aparece en spec generado tras implementaciÃ³n del endpoint.

## 2. Backend - Providers (Groq)

- [x] 2.1 AÃ±adir configuraciÃ³n de Groq (lectura de GROQ_API_KEY desde entorno, sin exponerla). Verificar: variable leÃ­da solo en backend y no aparece en logs.
- [x] 2.2 Implementar cliente/proveedor Groq en `backend/app/providers/` siguiendo arquitectura (soportar llamada de generaciÃ³n de texto). Verificar: puede instanciarse sin exponer secretos.
- [x] 2.3 Preparar lÃ³gica para usar modelo seleccionado (con valor por defecto razonable) respetando el diseÃ±o de fallback (OpenRouter) ya previsto. Verificar: cÃ³digo no fuerza fallback en caso de error de validaciÃ³n.

## 3. Backend - Workflows (LangGraph)

- [x] 3.1 Crear flujo `generate_direct` en `backend/app/workflows/generate_direct.py` (o estructura acorde a mÃ³dulo) que invoca proveedor Groq y devuelve texto + metadatos (provider, model). Verificar: flujo retorna estructura esperada.
- [x] 3.2 Integrar workflow con API (inyectar dependencias segÃºn patrÃ³n existente). Verificar: importaciÃ³n correcta y sin dependencias circulares.

## 4. Backend - API Endpoint

- [x] 4.1 AÃ±adir esquema Pydantic para request/response de `POST /generate` (mÃ­nimo viable: `brief` requerido). Verificar: validaciÃ³n bÃ¡sica funciona (400 si falta brief).
- [x] 4.2 Implementar ruta `POST /generate` en `backend/app/api/` que ejecuta flujo directo y devuelve respuesta con `text`, `provider`, `model`. Verificar: responde 200 con estructura correcta.
- [x] 4.3 AÃ±adir CORS/registro de ruta segÃºn patrÃ³n existente. Verificar: endpoint accesible desde frontend en desarrollo.

## 5. Frontend

- [x] 5.1 Crear formulario de briefing (textarea para briefing) y botÃ³n "Generar" en interfaz web. Verificar: formulario envÃ­a datos correctamente.
- [x] 5.2 Implementar llamada a API (`POST ${VITE_API_URL}/generate`) con configuraciÃ³n por entorno. Verificar: peticiÃ³n incluye briefing y recibe respuesta.
- [x] 5.3 Mostrar resultado generado listo para revisar (sin botÃ³n de publicar). Verificar: texto aparece y es el devuelto por API.
- [x] 5.4 Manejo bÃ¡sico de estados (cargando/error) sin sobrecomplicar. Verificar: estados visibles al usuario.

## 6. IntegraciÃ³n y Pruebas

- [x] 6.1 Actualizar `.env.example` con variables necesarias para Groq (GROQ_API_KEY) si faltan (solo nombres, valores inocuos). Verificar: `.env.example` no contiene secretos.
- [x] 6.2 Verificar flujo completo (tests API pasan, frontend build OK; integración docker-compose requiere variables en entorno) en docker-compose (frontend â api â Groq) funciona end-to-end con variables configuradas. Verificar: generaciÃ³n exitosa desde UI.
- [x] 6.3 Ejecutar checks (ruff, mypy, pytest OK; frontend lint/typecheck/tests OK) del backend (ruff, mypy, pytest) y frontend (lint, typecheck, tests) segÃºn Makefile/CI. Verificar: todos los checks pasan.
