# API HTTP

- **Estado:** Aceptado
- **Versión:** 0.3.0
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



## `POST /generate`

Genera una publicación de LinkedIn a partir de un briefing enviado por el frontend.

### Entrada

`application/json`:

| Campo | Tipo | Obligatorio | Significado |
|---|---|---|---|
| `brief` | `string` | Sí | Briefing del usuario que describe el tema e instrucciones |
| `audience` | `string` (enum) | Sí | Audiencia destinataria. Valores permitidos: `tech-professionals`, `ai-specialists`, `business-leaders`, `general-audience` |
| `tone` | `string` (enum) | Sí | Tono de la publicación. Valores permitidos: `professional`, `friendly`, `inspiring`, `educational` |

### Salida

`200 OK` con `application/json`:

| Campo | Tipo | Significado |
|---|---|---|
| `text` | `string` | Texto generado listo para revisar |
| `provider` | `string` | Proveedor utilizado (ej. `groq`) |
| `model` | `string` | Modelo utilizado |

### Errores

| Código | Cuándo ocurre | Qué debe hacer el consumidor |
|---|---|---|
| `422 Unprocessable Entity` | Falta `brief`, está vacío o solo contiene espacios, `audience` o `tone` faltan o no son un valor permitido, o el cuerpo no es válido | No enviar un briefing vacío ni valores fuera de los permitidos; indicar al usuario que revise el briefing y las opciones |
| `500 Internal Server Error` | Error en la generación (por ejemplo, fallo del proveedor) | Informar del fallo sin mostrar detalles internos y conservar el briefing para reintentar |

## Compatibilidad

Añadir endpoints o campos opcionales a una respuesta sube la versión MINOR. Quitar o renombrar endpoints o campos, o cambiar su tipo, es incompatible: sube la MAJOR y requiere un ADR o una nota de migración.
