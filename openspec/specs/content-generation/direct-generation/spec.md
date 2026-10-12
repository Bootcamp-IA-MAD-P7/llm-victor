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

### Requirement: Añadir contexto opcional a una generación (RF-02)

El sistema SHALL permitir al usuario aportar un contexto adicional opcional antes de generar, SHALL tenerlo en cuenta en el contenido devuelto y SHALL tratar ese contexto como un dato del usuario separado de las instrucciones del sistema, sin que las sustituya. El campo y el formato de la solicitud se definen en el contrato `docs/CONTRACTS/api.md`.

#### Scenario: Generar con contexto

- **WHEN** el usuario escribe un contexto adicional y envía el briefing
- **THEN** la solicitud de generación incluye ese contexto
- **THEN** el texto generado tiene en cuenta el contexto aportado en medida razonable para esta versión

#### Scenario: Generar sin contexto

- **WHEN** el usuario deja el contexto vacío o no lo aporta y envía el briefing
- **THEN** la generación se completa igual que sin contexto
- **THEN** la ausencia de contexto no produce ningún error

#### Scenario: El contexto no sustituye las instrucciones del sistema

- **WHEN** el contexto incluye texto que podría interpretarse como instrucciones
- **THEN** el contexto se incorpora como dato del usuario, en un bloque separado de las instrucciones del sistema
- **THEN** no reemplaza la configuración de la generación ni la consigna de generar una publicación de LinkedIn

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
