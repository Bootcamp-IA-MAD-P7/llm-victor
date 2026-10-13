## ADDED Requirements

### Requirement: Conexión de la API a Qdrant por configuración

La API SHALL tomar la dirección de Qdrant y su clave opcional del entorno, sin suponer una instancia local, y SHALL indicar en un endpoint propio si llega a Qdrant con esa configuración, según el [contrato de la API](/docs/CONTRACTS/api.md). Ese endpoint SHALL NOT exponer la clave ni detalles internos de la conexión.

Implementa: RNF-05, [ADR-0001](/docs/ADR/0001-docker-first-deployable-services.md).

#### Scenario: Qdrant accesible

- **WHEN** la API está configurada con la dirección y la clave de un Qdrant que responde, y se consulta su estado de Qdrant
- **THEN** responde con éxito e indica que Qdrant está disponible

#### Scenario: Qdrant externo

- **WHEN** se arranca la API configurada con la dirección y la clave de un Qdrant distinto del local, sin cambiar su código ni su imagen
- **THEN** el estado de Qdrant indica que está disponible

#### Scenario: Qdrant no accesible

- **WHEN** Qdrant no responde, la dirección es incorrecta o la clave no es válida, y se consulta el estado de Qdrant
- **THEN** la API responde que Qdrant no está disponible, sin mostrar la clave ni detalles internos, y su endpoint de salud general sigue respondiendo con éxito

#### Scenario: Entorno local

- **WHEN** la persona ejecuta `make up` sin configurar Qdrant
- **THEN** la API se conecta al Qdrant del entorno local

### Requirement: Imagen de producción de la API

La API SHALL tener una imagen de producción que se construye por separado del entorno local, sin herramientas de desarrollo, que no se ejecuta como root, escucha en el puerto que indica el entorno y toma toda su configuración (orígenes CORS, secretos de proveedores y conexión a Qdrant) del entorno.

Implementa: RNF-05, [ADR-0001](/docs/ADR/0001-docker-first-deployable-services.md).

#### Scenario: Construcción por separado

- **WHEN** la persona construye la imagen de producción de la API
- **THEN** obtiene una imagen sin levantar Compose ni el resto de servicios

#### Scenario: Puerto del entorno

- **WHEN** se ejecuta la imagen con un puerto definido en el entorno
- **THEN** la API responde en ese puerto, y en el 8000 si no se define

#### Scenario: Configuración en tiempo de ejecución

- **WHEN** se ejecuta la misma imagen con otros orígenes CORS, otras claves de proveedores u otro Qdrant
- **THEN** la API aplica esa configuración sin reconstruir la imagen
