# content-generation/direct-generation

## ADDED Requirements

### Requirement: Seleccionar el modelo de generación (RF-05)

El sistema SHALL permitir al usuario elegir uno de los modelos del catálogo antes de generar, SHALL usar ese modelo en la generación y SHALL rechazar con un error de validación (4xx) un modelo que no está en el catálogo, sin ejecutar la generación. Elegir un modelo NO SHALL generar varias respuestas ni comparar modelos. El campo y el formato de la solicitud se definen en el contrato `docs/CONTRACTS/api.md`.

#### Scenario: La web ofrece el selector de modelo con las opciones del catálogo

- **WHEN** el usuario abre el formulario de generación y el catálogo de modelos está disponible
- **THEN** puede elegir entre las opciones del catálogo, cada una con su etiqueta legible
- **THEN** hay un modelo seleccionado por defecto

#### Scenario: El modelo elegido llega a la API y se usa en la generación

- **WHEN** el usuario elige un modelo del catálogo y envía el briefing
- **THEN** la solicitud de generación incluye ese modelo
- **THEN** la generación usa el modelo elegido
- **THEN** la respuesta informa del modelo efectivo utilizado

#### Scenario: La API rechaza un modelo fuera del catálogo

- **WHEN** la API recibe un modelo ausente o que no está en el catálogo configurado
- **THEN** la API responde con un error de validación (código 4xx)
- **THEN** la API NO ejecuta la generación

#### Scenario: Elegir un modelo no multiplica las respuestas

- **WHEN** el usuario elige un modelo y genera
- **THEN** el sistema produce una sola generación
- **THEN** el sistema no compara modelos ni devuelve varias respuestas

### Requirement: Comunicar un modelo no disponible (RF-05)

Cuando el modelo elegido deja de estar disponible, el sistema SHALL comunicarlo de forma comprensible y SHALL permitir elegir otro, sin sustituir el modelo automáticamente por otro.

#### Scenario: El sistema comunica que el modelo ya no está disponible

- **WHEN** el modelo elegido estaba en el catálogo pero el proveedor lo rechaza como no disponible durante la generación
- **THEN** la API responde con un error que identifica el modelo como no disponible, distinto de un fallo genérico de generación
- **THEN** la web muestra un mensaje comprensible
- **THEN** no se devuelve contenido generado

#### Scenario: El usuario puede elegir otro modelo tras el aviso

- **WHEN** la web comunica que el modelo no está disponible
- **THEN** el usuario puede elegir otro modelo del catálogo y volver a generar
- **THEN** el sistema no recurre por su cuenta a otro modelo
