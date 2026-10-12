## 1. API: validación del briefing

- [x] 1.1 Añadir a `GenerateRequest` un validador que recorte `brief` y rechace el resultado vacío; verificar con tests que `""`, `"   "` y el campo ausente devuelven `422` y no ejecutan la generación.
- [x] 1.2 Propagar los fallos reales del proveedor Groq (dejar de convertirlos en `[FALLBACK-STUB]`), conservando el stub solo cuando falta `GROQ_API_KEY`; verificar con un test que mockea el workflow para lanzar y comprueba la respuesta `500`.
- [x] 1.3 Confirmar que el error `500` no filtra detalles internos; verificar con un test que el detalle es genérico y no contiene información del proveedor.

## 2. Web: validación, carga y errores

- [x] 2.1 Validar el briefing no vacío en `briefing-form` antes de enviar, mostrar un mensaje y no llamar a la API; verificar con un test de componente que el fetch no se invoca.
- [x] 2.2 Introducir en `lib/api.ts` un error tipado con el `status` y traducir a mensajes distintos el fallo de conexión/API y el fallo de generación (`5xx`); verificar con tests unitarios.
- [x] 2.3 Mostrar el estado de carga mientras se genera y deshabilitar el botón durante la petición; verificar con un test que el botón queda deshabilitado y el estado visible.
- [x] 2.4 Ante un fallo, mostrar un error comprensible y conservar el briefing escrito; verificar con un test que el `textarea` mantiene el texto tras el error y permite reintentar.

## 3. Contrato y documentación

- [x] 3.1 Documentar en `docs/CONTRACTS/api.md` los errores de `POST /generate` (`422` para briefing ausente/vacío/en blanco y `500` para fallo de generación) junto al contrato de generación; verificar que la tabla incluye ambos códigos y qué debe hacer el consumidor.

## 4. Verificación final

- [x] 4.1 Ejecutar los checks del proyecto (`npm run check` y `npm run build` en la web; `ruff`, `mypy` y `pytest` en la API) y `openspec validate`; verificar que todos pasan en verde.
