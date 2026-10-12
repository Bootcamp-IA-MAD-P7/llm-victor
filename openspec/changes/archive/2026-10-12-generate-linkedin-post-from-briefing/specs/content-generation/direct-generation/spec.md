## Purpose

Permite generar una publicación de LinkedIn directamente desde un briefing y parámetros mínimos, devolviendo un resultado revisable con información del proveedor y modelo usados.

## ADDED Requirements

### Requirement: Generar publicación desde briefing (RF-01, RF-03)

El sistema SHALL permitir a un usuario enviar un briefing y recibir una publicación de LinkedIn generada, lista para revisar, sin que el sistema la publique.

#### Scenario: Generación exitosa desde briefing
- **WHEN** el usuario envía un briefing no vacío a través del endpoint de generación
- **THEN** la API devuelve un texto correspondiente al tema e instrucciones del briefing
- **THEN** el texto está listo para revisar
- **THEN** el sistema NO publica el contenido en LinkedIn

#### Scenario: El contenido corresponde al briefing
- **WHEN** se genera contenido desde un briefing con tema e instrucciones específicas
- **THEN** el texto generado refleja dichas instrucciones en medida razonable para esta versión mínima
- **THEN** el resultado es utilizable para revisión

### Requirement: Entregar metadatos de generación

El sistema SHALL devolver información del proveedor y modelo utilizados en la generación.

#### Scenario: Metadatos presentes en respuesta
- **WHEN** la generación se completa con éxito
- **THEN** la respuesta incluye `provider` y `model` con los valores efectivos usados

### Requirement: Mantener secretos en el backend (seguridad)

El sistema SHALL garantizar que la clave de Groq solo reside en el backend (variables de entorno). El cliente frontend no deberá tener acceso directo a dicha clave.

#### Scenario: Clave aislada en backend
- **WHEN** el cliente frontend realiza una petición de generación
- **THEN** la llamada a Groq se realiza exclusivamente desde el backend
- **THEN** ninguna clave de proveedor se expone al navegador

### Requirement: Contrato de generación registrado

El sistema SHALL tener el contrato `frontend` → `api` de generación registrado en `docs/CONTRACTS/`.

#### Scenario: Contrato documentado
- **WHEN** se implementa el endpoint de generación
- **THEN** `docs/CONTRACTS/api.md` incluye la especificación del endpoint (método, ruta, solicitud, respuesta y errores mínimos)
