# API HTTP

- **Estado:** Aceptado
- **Versión:** 0.9.0
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

## `GET /health/qdrant`

Indica si la API llega a Qdrant con su configuración actual (`QDRANT_URL` y `QDRANT_API_KEY`, [ARCHITECTURE §6](../ARCHITECTURE.md#6-datos-configuración-y-secretos)): Qdrant debe responder y aceptar la clave. Sirve para comprobar el despliegue; la web no lo consume.

### Entrada

Ninguna.

### Salida

`200 OK` con:

| Campo | Tipo | Significado |
|---|---|---|
| `status` | `"ok"` | Qdrant responde y acepta la clave configurada |

### Errores

| Código | Cuándo ocurre | Qué debe hacer el consumidor |
|---|---|---|
| `503 Service Unavailable` | Qdrant no responde en 3 s, la URL no es válida o la clave falta o no es correcta. El cuerpo es `{"detail": "Qdrant is not available"}`, sin la clave ni detalles internos; la causa queda en el log de la API | Revisar `QDRANT_URL`, `QDRANT_API_KEY` y el estado de Qdrant. `GET /health` sigue respondiendo `200` |

## `GET /models`

Devuelve el catálogo de modelos de texto disponibles para la generación, configurados en la API: primero los de Groq (`TEXT_MODELS`) y después los de OpenRouter (`OPENROUTER_MODELS`). No expone secretos ni detalles internos del proveedor; la etiqueta puede nombrar el proveedor.

### Entrada

Ninguna.

### Salida

`200 OK` con `application/json`:

| Campo | Tipo | Significado |
|---|---|---|
| `models` | `array` | Modelos disponibles |
| `models[].id` | `string` | Identificador estable del modelo |
| `models[].label` | `string` | Etiqueta legible para el usuario |

### Errores

| Código | Cuándo ocurre | Qué debe hacer el consumidor |
|---|---|---|
| Sin respuesta o error de red | La API no está en marcha o no es accesible | Indicar que no se pudieron cargar los modelos disponibles |

## `POST /generate`

Genera una publicación de LinkedIn a partir de un briefing enviado por el frontend.

Cada modelo del catálogo pertenece a un proveedor. Con un modelo de Groq, ante una indisponibilidad, un límite o un *rate limit* de Groq, la API recurre una vez a OpenRouter con sus modelos configurados en orden y responde con el resultado de OpenRouter; si ambos proveedores fallan, la generación falla. Los errores de validación de la solicitud y un modelo que Groq ya no ofrece no activan el recurso a OpenRouter. Con un modelo de OpenRouter, la API llama a OpenRouter con ese modelo primero y los demás configurados detrás, y OpenRouter pasa al siguiente si uno falla o está limitado.

### Entrada

`application/json`:

| Campo | Tipo | Obligatorio | Significado |
|---|---|---|---|
| `brief` | `string` | Sí | Briefing del usuario que describe el tema e instrucciones |
| `audience` | `string` (enum) | Sí | Audiencia destinataria. Valores permitidos: `tech-professionals`, `ai-specialists`, `business-leaders`, `general-audience` |
| `tone` | `string` (enum) | Sí | Tono de la publicación. Valores permitidos: `professional`, `friendly`, `inspiring`, `educational` |
| `language` | `string` (enum) | Sí | Idioma de salida del contenido. Valores permitidos: `es`, `en`, `fr`, `it` |
| `model` | `string` | Sí | Identificador del modelo elegido del catálogo devuelto por `GET /models`. Debe estar entre los modelos configurados; la generación usa ese modelo |
| `context` | `string` | No | Contexto adicional aportado por el usuario. Se trata como dato del usuario y no sustituye las instrucciones del sistema. Si falta o está vacío, la generación no lo usa |

### Salida

`200 OK` con `application/json`:

| Campo | Tipo | Significado |
|---|---|---|
| `text` | `string` | Texto generado listo para revisar |
| `provider` | `string` | Proveedor que generó el texto: `groq` u `openrouter` (por elección del modelo o por fallback) |
| `model` | `string` | Modelo efectivo utilizado, que puede diferir del solicitado cuando el fallback o el enrutado de OpenRouter cambian de modelo |

### Errores

| Código | Cuándo ocurre | Qué debe hacer el consumidor |
|---|---|---|
| `422 Unprocessable Entity` | Falta `brief`, está vacío o solo contiene espacios, `audience`, `tone`, `language` o `model` faltan o no son un valor permitido (`model` fuera del catálogo), o el cuerpo no es válido | No enviar un briefing vacío ni valores fuera de los permitidos; indicar al usuario que revise el briefing y las opciones |
| `409 Conflict` | El `model` estaba en el catálogo pero el proveedor ya no lo ofrece (modelo retirado o inexistente) | Comunicar que el modelo ya no está disponible y permitir elegir otro; conservar el briefing. El sistema no sustituye el modelo automáticamente |
| `500 Internal Server Error` | Error en la generación (por ejemplo, fallo del proveedor; también si Groq falla y OpenRouter no completa el fallback) | Informar del fallo sin mostrar detalles internos y conservar el briefing para reintentar |

## Compatibilidad

Añadir endpoints o campos opcionales a una respuesta sube la versión MINOR. Quitar o renombrar endpoints o campos, o cambiar su tipo, es incompatible: sube la MAJOR y requiere un ADR o una nota de migración.
