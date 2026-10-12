## Why

La historia #14 requiere poder generar la publicación en español, inglés, francés o italiano (RF-04), y que la elección llegue al contenido devuelto (RF-02). Hoy el prompt no fija idioma y la petición no lo transporta, así que el resultado depende del idioma en que hable el modelo.

## What Changes

- La petición `POST /generate` acepta un campo `language` (enum) con los valores `es`, `en`, `fr` e `it`, obligatorio, con `es` como valor por defecto en la web.
- El frontend ofrece un selector de idioma con las cuatro opciones, español seleccionado por defecto.
- El prompt de generación directa indica el idioma de salida elegido.
- La API rechaza un idioma no válido con un error de validación (422) y no ejecuta la generación.
- El contrato `docs/CONTRACTS/api.md` documenta el nuevo campo `language` (versión 0.5.0).

## Capabilities

### New Capabilities

Ninguna.

### Modified Capabilities

- `content-generation/direct-generation`: la generación acepta y aplica el idioma elegido, con los cuatro valores permitidos y el rechazo de valores no válidos.

## Impact

- `docs/CONTRACTS/api.md`: nuevo campo `language` en `POST /generate` (sube a 0.5.0).
- `backend/app/api/generate.py`: modelo de petición con `language`.
- `backend/app/workflows/generate_direct.py`: enumerado `Language`, etiquetas y prompt con idioma.
- `frontend/src/lib/api.ts` y `frontend/src/lib/generation-options.ts`: tipo y opciones de idioma.
- `frontend/src/components/briefing-form.tsx`: selector de idioma.
- Tests de API y de frontend para los cuatro idiomas, el valor por defecto y el rechazo de valores no válidos.
- `openspec/specs/content-generation/direct-generation/spec.md`: requisito delta sincronizado al publicar.