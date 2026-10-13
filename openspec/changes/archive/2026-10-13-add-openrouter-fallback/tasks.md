# Tareas — add-openrouter-fallback

## 1. Configuración y cliente de OpenRouter

- [x] 1.1 Añadir `openrouter_model` a `backend/app/config.py` y `OPENROUTER_MODEL` a `.env.example`; verificar con un test que `Settings` lee el valor (por defecto `meta-llama/llama-3.1-8b-instruct`) y permite sobreescribirlo por entorno.
- [x] 1.2 Declarar `httpx` como dependencia directa en `backend/pyproject.toml` y actualizar `uv.lock`; verificar que `uv sync --frozen` (o el check del CI) sigue funcionando.
- [x] 1.3 Implementar `OpenRouterProvider` en `backend/app/providers/openrouter.py`: sin clave devuelve un *stub* con `provider: "openrouter"` y el modelo configurado; con clave llama a `POST {base_url}/chat/completions` con `httpx` y un *timeout*. Verificar con test del *stub* (sin red) y con un test que comprueba la petición con `httpx` simulado.

## 2. Pasarela de proveedores con fallback elegible

- [x] 2.1 Implementar la clasificación de fallos elegibles (sin estado HTTP, `429`, `≥ 500` → elegible; `4xx` y `ModelUnavailableError` → no) y verificar con test parametrizado que cubre cada caso.
- [x] 2.2 Implementar `TextProviderGateway` en `backend/app/providers/gateway.py` (intenta Groq y, solo ante un fallo elegible, recurre a OpenRouter una vez) y verificar con tests que: el éxito primario no llama al fallback; un fallo elegible devuelve el resultado del fallback; un fallo no elegible se propaga; si ambos fallan, se propaga el error sin reintentar.

## 3. Integración con la API y el flujo de generación

- [x] 3.1 Construir la pasarela desde `Settings` en `backend/app/api/generate.py` y pasarla a `generate_direct`; verificar con test que, cuando Groq falla con un error elegible, `POST /generate` responde `200` con `provider: "openrouter"` y el modelo efectivo, y que un error de validación o un modelo no disponible no activan el fallback (`422`/`409`).
- [x] 3.2 Actualizar `docs/CONTRACTS/api.md` a la versión 0.8.0 documentando que `provider` puede ser `groq` o `openrouter` y que el fallback solo se activa ante fallos elegibles; verificar que la sección de `POST /generate` describe el comportamiento y mantiene los códigos de error actuales.

## 4. Verificación e integración

- [x] 4.1 Ejecutar `openspec validate`, `sync` y `make check` (ruff, ruff format, mypy, pytest y checks del frontend); confirmar que los criterios de aceptación de #18 quedan cubiertos y que la web sigue mostrando el proveedor y el modelo efectivos sin cambios.

## Workflow follow-up

- Archivar el cambio tras aprobar la revisión del PR (WORKFLOW §6, parada 4).
- Verificar el resultado archivado.
