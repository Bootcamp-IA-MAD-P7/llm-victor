## ADDED Requirements

### Requirement: Configurar la audiencia y el tono de una generación (RF-02)

El sistema SHALL permitir al usuario consultar y cambiar la audiencia y el tono de una generación antes de generarla, SHALL aplicar esos valores al contenido devuelto y SHALL rechazar los valores no permitidos. Los valores permitidos y el formato de la solicitud se definen en el contrato `docs/CONTRACTS/api.md`.

#### Scenario: La web ofrece audiencia y tono antes de generar
- **WHEN** el usuario abre el formulario de generación
- **THEN** puede consultar y cambiar la audiencia y el tono antes de generar
- **THEN** cada opción se muestra con una etiqueta comprensible para el usuario

#### Scenario: Los valores llegan a la API y se aplican al resultado
- **WHEN** el usuario elige una audiencia y un tono válidos y envía el briefing
- **THEN** la solicitud de generación incluye esos valores
- **THEN** el texto generado refleja la audiencia y el tono elegidos en medida razonable para esta versión

#### Scenario: La API rechaza valores no válidos
- **WHEN** la API recibe una audiencia o un tono que no está entre los valores permitidos
- **THEN** la API responde con un error de validación (código 4xx)
- **THEN** la API NO ejecuta la generación
