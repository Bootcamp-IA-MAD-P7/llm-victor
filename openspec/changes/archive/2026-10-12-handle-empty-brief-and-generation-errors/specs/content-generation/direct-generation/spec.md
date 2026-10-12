## ADDED Requirements

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

## MODIFIED Requirements

### Requirement: Contrato de generación registrado

El sistema SHALL tener el contrato `frontend` → `api` de generación y su contrato de error registrados en `docs/CONTRACTS/`.

#### Scenario: Contrato documentado
- **WHEN** se implementa el endpoint de generación
- **THEN** `docs/CONTRACTS/api.md` incluye la especificación del endpoint (método, ruta, solicitud, respuesta y errores mínimos)

#### Scenario: Contrato de error documentado (RF-01, RNF-07)
- **WHEN** el endpoint rechaza un briefing vacío o falla la generación
- **THEN** `docs/CONTRACTS/api.md` documenta el código y el significado de cada error de generación, junto al contrato de generación
