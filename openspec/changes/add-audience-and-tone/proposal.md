## Why

Issue #12 (RF-02): el usuario debe poder orientar la publicación a una audiencia y un tono antes de generar. Hoy `POST /generate` solo acepta `brief`, así que la generación no puede adaptarse a ninguna de las dos opciones. Esta historia añade los selectores, amplía el contrato y ajusta el prompt para que el texto refleje ambos valores.

## What Changes

- Añadir selectores de **audiencia** y **tono** al formulario de la web, con las opciones acordadas.
- Ampliar `POST /generate` con los campos `audience` y `tone`, validados como valores permitidos; la API rechaza valores no válidos con `422`.
- Componer el prompt de generación directa con la audiencia y el tono además del briefing, de modo que el texto los refleje.
- Documentar los nuevos campos y sus valores en `docs/CONTRACTS/api.md` (sube la versión MINOR, `0.2.0` → `0.3.0`).

## Capabilities

### New Capabilities
- (ninguna)

### Modified Capabilities
- `content-generation/direct-generation`: se añade la configuración de audiencia y tono de una generación directa, su validación y su efecto en el resultado.

## Impact

- `backend/app/api/generate.py`: campos y validación de `audience`/`tone` en la solicitud.
- `backend/app/workflows/generate_direct.py`: el prompt incorpora audiencia y tono.
- `frontend/src/components/briefing-form.tsx` y `frontend/src/lib/api.ts`: selectores y envío de los nuevos campos.
- `docs/CONTRACTS/api.md`: `POST /generate` con `audience`/`tone` (MINOR).
- Tests de API y de componentes para los nuevos comportamientos.
