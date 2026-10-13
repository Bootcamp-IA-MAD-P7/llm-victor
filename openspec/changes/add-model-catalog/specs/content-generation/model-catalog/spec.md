# content-generation/model-catalog

## Purpose

Permite al usuario ver qué modelos de texto puede usar, publicando desde la API un catálogo de modelos configurados con identificadores estables y sin secretos, y mostrándolo en la web.

## ADDED Requirements

### Requirement: Publicar el catálogo de modelos disponibles (RF-05, RNF-05)

La API SHALL exponer el catálogo de modelos de texto disponibles para la tarea, cada uno con un identificador estable y una etiqueta legible, sin secretos ni detalles internos del proveedor. El endpoint y el formato de la respuesta se definen en el contrato `docs/CONTRACTS/api.md`.

#### Scenario: La API expone el catálogo configurado
- **WHEN** el frontend consulta el catálogo de modelos
- **THEN** la API responde con la lista de modelos configurados
- **THEN** cada modelo incluye un identificador estable y una etiqueta legible

#### Scenario: El catálogo no contiene secretos
- **WHEN** la API responde el catálogo de modelos
- **THEN** la respuesta no incluye claves ni credenciales de proveedores
- **THEN** la respuesta no expone detalles internos del proveedor

### Requirement: Mostrar los modelos disponibles en la web (RF-05, RNF-07)

El sistema SHALL mostrar al usuario las opciones de modelo disponibles obtenidas del catálogo de la API, y SHALL comunicar de forma comprensible si el catálogo no se puede cargar.

#### Scenario: La web muestra las opciones del catálogo
- **WHEN** la web obtiene el catálogo de modelos
- **THEN** muestra al usuario las opciones disponibles con su etiqueta legible

#### Scenario: La web comunica que no puede cargar el catálogo
- **WHEN** la web no puede obtener el catálogo de modelos
- **THEN** comunica al usuario que no se pudieron cargar los modelos disponibles