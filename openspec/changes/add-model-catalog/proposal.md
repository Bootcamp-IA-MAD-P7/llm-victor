## Why

La historia #15 requiere que el usuario vea qué modelos de texto puede usar (RF-05). Hoy la API solo conoce un modelo fijo (`DEFAULT_MODEL_GROQ`) y no publica ninguna lista, así que la web no puede mostrar opciones ni existe una base estable sobre la que #16 valide y use el modelo elegido.

## What Changes

- La API expone `GET /models`: el catálogo de modelos de texto configurados, cada uno con un identificador estable y una etiqueta legible, sin secretos ni detalles internos del proveedor.
- El catálogo se define por configuración de la API (variable de entorno) con valores por defecto inocuos, siguiendo el patrón de `.env.example`.
- El frontend consulta el catálogo y muestra al usuario las opciones disponibles.
- El contrato `docs/CONTRACTS/api.md` documenta el endpoint `GET /models` (sube a 0.6.0).

## Capabilities

### New Capabilities

- `content-generation/model-catalog`: la API publica el catálogo de modelos de texto disponibles con identificadores estables y sin secretos, y la web muestra esas opciones al usuario.

### Modified Capabilities

Ninguna.

## Impact

- `docs/CONTRACTS/api.md` y `docs/CONTRACTS/README.md`: nuevo endpoint `GET /models` (versión 0.6.0).
- `backend/app/`: módulo y endpoint del catálogo, más la configuración de la lista de modelos.
- `backend/tests/`: tests del catálogo y del endpoint.
- `frontend/src/`: consulta del catálogo y presentación de las opciones, con sus tests.
- `.env.example`: variable que define los modelos del catálogo.
- `openspec/specs/content-generation/model-catalog/spec.md`: spec nueva, sincronizada al publicar.
