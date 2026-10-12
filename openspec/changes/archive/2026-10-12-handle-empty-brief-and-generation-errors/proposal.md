## Why

Issue #10: cuando no se puede generar contenido, el usuario debe entender por qué y no perder lo que escribió. Hoy la web descarta en silencio un briefing vacío y la API acepta una cadena en blanco; ante un fallo, la web muestra un mensaje genérico sin distinguir la causa. Esto completa los errores del flujo de generación directa abierto en #9 (RF-01, RNF-07).

## What Changes

- Rechazar el briefing vacío o en blanco en la web (no se envía y se avisa al usuario) y en la API (respuesta de error de validación, no `200`).
- Mostrar un estado de carga explícito mientras se genera.
- Ante un fallo de generación, mostrar un error comprensible y conservar el briefing ya escrito en el formulario.
- Documentar el contrato de error de `POST /generate` en `docs/CONTRACTS/api.md`, junto al contrato de generación.

## Capabilities

### New Capabilities
- (ninguna)

### Modified Capabilities
- `content-generation/direct-generation`: se precisan los requisitos de validación del briefing, estado de carga y comunicación de errores sin perder el briefing, y su contrato de error.

## Impact

- `backend/app/api/`: validación del briefing y respuestas de error de `POST /generate`.
- `frontend/`: validación en el formulario, estado de carga, mensaje de error y conservación del briefing.
- `docs/CONTRACTS/api.md`: errores de `POST /generate` (documentación, sin cambio de versión si no varía la interfaz observable ya descrita).
- Tests de API y de componentes de la web para los nuevos comportamientos.
