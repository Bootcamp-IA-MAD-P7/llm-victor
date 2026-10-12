# content-generation/direct-generation

## ADDED Requirements

### Requirement: Seleccionar el idioma de salida (RF-04, RF-02)

El sistema SHALL permitir al usuario elegir español, inglés, francés o italiano como idioma de salida antes de generarla, SHALL devolver el contenido en ese idioma y SHALL rechazar los valores no permitidos. Los valores permitidos y el formato de la solicitud se definen en el contrato `docs/CONTRACTS/api.md`.

#### Scenario: La web ofrece los cuatro idiomas con español por defecto
- **WHEN** el usuario abre el formulario de generación
- **THEN** puede elegir español, inglés, francés e italiano
- **THEN** la opción seleccionada por defecto es español

#### Scenario: El idioma llega a la API y determina el contenido
- **WHEN** el usuario elige un idioma válido y envía el briefing
- **THEN** la solicitud de generación incluye ese idioma
- **THEN** el texto generado se produce en el idioma elegido en medida razonable para esta versión

#### Scenario: La API rechaza un idioma no válido
- **WHEN** la API recibe un idioma que no está entre los valores permitidos
- **THEN** la API responde con un error de validación (código 4xx)
- **THEN** la API NO ejecuta la generación