# content-generation/direct-generation Specification

## Purpose
Permite generar una publicación de LinkedIn directamente desde un briefing y parámetros mínimos, devolviendo un resultado revisable con información del proveedor y modelo usados.

## Requirements

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

El sistema SHALL tener el contrato `frontend` → `api` de generación y su contrato de error registrados en `docs/CONTRACTS/`.

#### Scenario: Contrato documentado
- **WHEN** se implementa el endpoint de generación
- **THEN** `docs/CONTRACTS/api.md` incluye la especificación del endpoint (método, ruta, solicitud, respuesta y errores mínimos)

#### Scenario: Contrato de error documentado (RF-01, RNF-07)
- **WHEN** el endpoint rechaza un briefing vacío o falla la generación
- **THEN** `docs/CONTRACTS/api.md` documenta el código y el significado de cada error de generación, junto al contrato de generación

### Requirement: Rechazar un briefing vacío (RF-01)

El sistema SHALL rechazar las solicitudes de generación cuyo briefing esté vacío o contenga solo espacios, tanto en la web como en la API.

#### Scenario: La web no envía un briefing vacío
- **WHEN** el usuario intenta generar con el campo de briefing vacío o solo con espacios
- **THEN** la web NO realiza la petición de generación
- **THEN** la web indica al usuario que debe escribir un briefing

#### Scenario: La API rechaza un briefing vacío
- **WHEN** la API recibe una solicitud de generación con `brief` ausente, vacío o solo con espacios
- **THEN** la API responde con un error de validación (código 4xx)
- **THEN** la API NO ejecuta la generación

### Requirement: Estado de carga durante la generación (RF-01)

El sistema SHALL indicar que la generación está en curso mientras espera el resultado.

#### Scenario: La web muestra un estado de carga
- **WHEN** el usuario envía un briefing válido y la generación está en curso
- **THEN** la web muestra un estado de carga
- **THEN** el estado de carga desaparece cuando llega el resultado o el error

### Requirement: Comunicar fallos de generación sin perder el briefing (RNF-07)

El sistema SHALL comunicar de forma comprensible un fallo de generación en la web, conservando el briefing que el usuario escribió.

#### Scenario: Fallo de generación comprensible
- **WHEN** la generación falla por un error de la API o del proveedor
- **THEN** la web muestra un mensaje de error comprensible
- **THEN** la web NO muestra detalles internos ni secretos

#### Scenario: El formulario se conserva tras el fallo
- **WHEN** la web muestra un error de generación
- **THEN** el briefing escrito sigue en el formulario
- **THEN** el usuario puede reintentar sin volver a escribirlo
