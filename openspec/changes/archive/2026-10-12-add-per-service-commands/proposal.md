## Why

Hoy el Makefile solo ofrece comandos para operar el conjunto de servicios: para reiniciar, ver los logs o abrir una consola en uno de ellos hay que tocar los tres. La épica [#2](https://github.com/Glezino/ai-content-generator/issues/2) (I1-E1) prevé operar cada servicio por separado, y [ARCHITECTURE §7](/docs/ARCHITECTURE.md#7-entorno-local-y-operación) ya lo describe como objetivo.

Historia [#11](https://github.com/Glezino/ai-content-generator/issues/11). No implementa ningún RF directamente: es herramienta de desarrollo que habilita la operación del walking skeleton descrita en [ADR-0001](/docs/ADR/0001-docker-first-deployable-services.md).

## What Changes

- Añadir al `Makefile` targets por servicio (`frontend`, `api` y `qdrant`) para construir o descargar la imagen, arrancar, detener, reiniciar, consultar el estado, ver los logs y abrir una consola.
- Qdrant usa `pull` en lugar de `build`, porque su imagen se descarga y no se construye.
- Añadir un target separado y explícito para borrar los volúmenes; ningún otro comando los elimina.
- Mantener los comandos con GNU Make en Windows, macOS y Linux, sin sintaxis exclusiva de Bash.
- Actualizar `make help` y [ARCHITECTURE §7](/docs/ARCHITECTURE.md#7-entorno-local-y-operación) con los comandos que pasan a ser Actual.
- Los comandos globales existentes no cambian.

## Capabilities

### New Capabilities

Ninguna.

### Modified Capabilities

Ninguna: es herramienta del entorno de desarrollo y no cambia el comportamiento observable de los servicios ni del sistema. El cambio se acoge a `skip_specs: true` en su `.openspec.yaml`.

## Impact

- **Makefile:** nuevos targets por servicio y de borrado de volúmenes.
- **Documentación:** ARCHITECTURE §7 (comandos del Makefile). README y las specs no cambian.
- **Servicios, contratos, ADR y specs:** sin cambios.
