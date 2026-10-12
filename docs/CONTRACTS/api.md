# API HTTP

- **Estado:** Aceptado
- **Versión:** 0.1.0
- **Productor → consumidores:** `api` → `frontend`
- **Artefacto ejecutable:** ninguno. FastAPI publica el esquema OpenAPI en `/openapi.json` mientras la API está en marcha, pero este documento es la fuente de verdad.

## Propósito

Estabiliza las peticiones HTTP que la web hace a la API. Cada endpoint tiene su propia sección; la generación de contenido se añadirá en [#9](https://github.com/Glezino/ai-content-generator/issues/9).

La URL base es `VITE_API_URL` en la web. La API solo acepta peticiones de navegador desde los orígenes de `CORS_ORIGINS` ([ARCHITECTURE §6](../ARCHITECTURE.md#6-datos-configuración-y-secretos)).

## `GET /health`

Indica si la API está disponible. No comprueba dependencias externas.

### Entrada

Ninguna.

### Salida

`200 OK` con:

| Campo | Tipo | Significado |
|---|---|---|
| `status` | `"ok"` | La API está en marcha |

### Errores

| Código | Cuándo ocurre | Qué debe hacer el consumidor |
|---|---|---|
| Sin respuesta o error de red | La API no está en marcha o no es accesible | Indicar que la API no está disponible y permitir reintentar |

## Compatibilidad

Añadir endpoints o campos opcionales a una respuesta sube la versión MINOR. Quitar o renombrar endpoints o campos, o cambiar su tipo, es incompatible: sube la MAJOR y requiere un ADR o una nota de migración.
