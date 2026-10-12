## 1. API: campo opcional y transporte

- [x] 1.1 Añadir a `backend/app/api/generate.py` el campo opcional `context` con valor por defecto `None` y un `field_validator` que lo recorte y lo convierta en `None` si queda vacío; verificar con tests que una solicitud con contexto, sin contexto o con contexto solo de espacios se acepta y que el valor normalizado llega al workflow.
- [x] 1.2 Propagar `context` desde el endpoint a `generate_direct`; verificar con un test que el workflow recibe el contexto (o `None`).

## 2. API: prompt de generación

- [x] 2.1 Ampliar `build_prompt` en `backend/app/workflows/generate_direct.py` para aceptar `context: str | None` y añadir, solo si hay contexto, un bloque de dato etiquetado tras el briefing, separado de las instrucciones del sistema; verificar con un test (proveedor simulado) que el prompt incluye el contexto y su etiqueta cuando existe y no incluye el bloque cuando es `None`.

## 3. Web: campo de contexto y envío

- [x] 3.1 Añadir a `briefing-form.tsx` un `textarea` de «Contexto» opcional; verificar con un test de componente que se renderiza y permite escribir, sin bloquear la generación por estar vacío.
- [x] 3.2 Ampliar `GenerateRequest` en `lib/api.ts` con `context?: string` y omitirlo del cuerpo cuando está vacío; verificar con un test unitario que el cuerpo incluye `context` cuando tiene valor y no lo incluye cuando es vacío.
- [x] 3.3 Verificar con un test de componente que el contexto escrito llega a la llamada de generación y que una generación sin contexto no lo envía.

## 4. Contrato y documentación

- [x] 4.1 Documentar en `docs/CONTRACTS/api.md` el campo opcional `context` de `POST /generate` (significado y carácter opcional) y subir la versión a `0.4.0`; corregir la fila desactualizada de `docs/CONTRACTS/README.md` para que muestre la versión vigente; verificar que la tabla de entrada incluye `context` y que las dos versiones coinciden.

## 5. Verificación final

- [x] 5.1 Ejecutar los checks del proyecto (`npm run check` y `npm run build` en la web; `ruff check .`, `ruff format --check .`, `mypy` y `pytest` en la API) y `openspec validate --strict`; verificar que todos pasan en verde.
