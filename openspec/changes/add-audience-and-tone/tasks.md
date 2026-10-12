## 1. API: validación y contrato

- [x] 1.1 Definir en `backend/app/api/generate.py` los enums de audiencia (`tech-professionals`, `ai-specialists`, `business-leaders`, `general-audience`) y tono (`professional`, `friendly`, `inspiring`, `educational`), y añadirlos como campos obligatorios de `GenerateRequest`; verificar con tests que los valores válidos se aceptan y que una audiencia o un tono no permitidos devuelven `422` sin ejecutar la generación.
- [x] 1.2 Propagar `audience` y `tone` desde el endpoint al workflow de generación; verificar con un test que el workflow recibe ambos valores.

## 2. API: prompt de generación

- [x] 2.1 Ampliar `generate_direct` para recibir `audience` y `tone`, traducirlos a su etiqueta en español y componer el prompt con una línea de audiencia y otra de tono antes del briefing; verificar con un test (proveedor simulado) que el prompt incluye la etiqueta de audiencia y la de tono.

## 3. Web: selectores y envío

- [x] 3.1 Añadir a `briefing-form.tsx` los selectores de audiencia y tono con sus opciones y etiquetas, con valor inicial en la primera opción; verificar con un test de componente que se renderizan las cuatro opciones de cada selector y que se pueden cambiar.
- [x] 3.2 Ampliar `GenerateRequest` en `lib/api.ts` con `audience` y `tone` y enviarlos en la petición; verificar con un test unitario que el cuerpo incluye ambos campos con los valores elegidos.
- [x] 3.3 Verificar con un test de componente que los valores seleccionados llegan a la llamada de generación.

## 4. Contrato y documentación

- [x] 4.1 Documentar en `docs/CONTRACTS/api.md` los campos `audience` y `tone` de `POST /generate`, sus valores permitidos y el `422` por valor no válido, y subir la versión a `0.3.0`; verificar que la tabla de entrada y la de errores los incluyen.

## 5. Verificación final

- [x] 5.1 Ejecutar los checks del proyecto (`npm run check` y `npm run build` en la web; `ruff`, `mypy` y `pytest` en la API) y `openspec validate --strict`; verificar que todos pasan en verde.
