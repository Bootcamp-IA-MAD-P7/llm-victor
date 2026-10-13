## Why

Historia #18. Hoy, si Groq no está disponible o alcanza un límite, la generación falla y el usuario solo recibe un error, aunque ARCHITECTURE §5 prevé OpenRouter como proveedor alternativo. Recurrir a OpenRouter ante esos fallos permite completar la generación y cumple RNF-07 (comunicar los fallos externos de forma comprensible) sin exponer detalles internos.

## What Changes

- La API configura OpenRouter como proveedor alternativo: clave por entorno (ya existente) y modelo alternativo configurable (`OPENROUTER_MODEL`).
- La capa de proveedores intenta primero Groq y, solo ante fallos elegibles (indisponibilidad, límite o *rate limit*), recurre a OpenRouter una vez.
- Los errores de validación de la solicitud y el modelo retirado o inexistente de Groq (RF-05, respuesta `409`) NO activan el fallback.
- La respuesta informa del proveedor y el modelo efectivos, también cuando el fallback cambia de modelo (RNF-03).
- Si ambos proveedores fallan, la API devuelve un error comprensible sin detalles internos (RNF-07).
- El contrato `docs/CONTRACTS/api.md` documenta el proveedor alternativo y su versión sube MINOR.

## Capabilities

### New Capabilities

Ninguna.

### Modified Capabilities

- `content-generation/direct-generation`: se añade el recurso a OpenRouter ante fallos elegibles de Groq y la garantía de que la respuesta refleja el proveedor y modelo efectivos.

## Impact

- `backend/app/providers/`: nuevo cliente de OpenRouter y una pasarela de texto que aplica el fallback; el clasificador de fallos elegibles.
- `backend/app/workflows/generate_direct.py`: genera a través de la pasarela de proveedores.
- `backend/app/api/generate.py`: construye la pasarela a partir de `Settings`.
- `backend/app/config.py` y `.env.example`: `OPENROUTER_MODEL` (la clave `OPENROUTER_API_KEY` ya existe).
- `docs/CONTRACTS/api.md`: documenta el proveedor alternativo y sube a 0.8.0 (MINOR; la interfaz no cambia, se amplían los valores posibles de `provider`).
- Tests de proveedor, pasarela y API.
- Sin cambios en la web: ya muestra el proveedor y el modelo efectivos (#17). Sin ADR: implementa la dirección ya aceptada en ARCHITECTURE §5.
