# content-generation/direct-generation

## MODIFIED Requirements

### Requirement: Entregar metadatos de generación

El sistema SHALL devolver el proveedor y el modelo efectivos usados en una generación y SHALL mostrarlos en la web junto al resultado, sin persistirlos entre sesiones (RNF-03). Los campos de la respuesta se definen en el contrato `docs/CONTRACTS/api.md`.

#### Scenario: Metadatos presentes en respuesta
- **WHEN** la generación se completa con éxito
- **THEN** la respuesta incluye `provider` y `model` con los valores efectivos usados

#### Scenario: La web muestra el proveedor y el modelo junto al resultado
- **WHEN** la web recibe una generación completada con éxito
- **THEN** muestra junto al texto el proveedor y el modelo usados, con una etiqueta comprensible
- **THEN** no muestra los metadatos cuando no hay resultado
