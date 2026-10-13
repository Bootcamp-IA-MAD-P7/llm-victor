# deployable-services Specification

## Purpose

Construir cada servicio de aplicación para desplegarlo por separado, configurado desde fuera y sin depender de direcciones locales, según ADR-0001.

## Requirements

### Requirement: URL de la API configurable al compilar la web

La web SHALL tomar la URL de la API de la configuración del build. Un build de producción SHALL fallar con un mensaje que nombre la variable cuando la URL falta o no es una URL `http` o `https` absoluta, y SHALL NOT recurrir a `localhost` por defecto. El servidor de desarrollo SHALL seguir usando la API local cuando no se configura la URL.

Implementa: RNF-05, [ADR-0001](/docs/ADR/0001-docker-first-deployable-services.md).

#### Scenario: Build con URL de la API

- **WHEN** se construye la web para producción con la URL de la API `https://api.example.com`
- **THEN** la web compilada envía sus peticiones a la API (salud, catálogo de modelos y generación) a `https://api.example.com`

#### Scenario: Build sin URL de la API

- **WHEN** se construye la web para producción sin definir la URL de la API
- **THEN** el build falla e indica qué variable falta, sin generar una web que apunte a `localhost`

#### Scenario: URL de la API no válida

- **WHEN** se construye la web para producción con una URL de la API que no es `http` o `https` absoluta
- **THEN** el build falla e indica que el valor no es válido

#### Scenario: Desarrollo local sin configuración

- **WHEN** la persona ejecuta `make up` sin definir la URL de la API
- **THEN** la web de desarrollo se comunica con la API local

### Requirement: Imagen de producción de la web

La web SHALL tener una imagen de producción que se construye por separado del entorno local, recibe la URL de la API como argumento de build y sirve la web compilada, incluido el fallback de rutas de la SPA.

Implementa: RNF-05, [ADR-0001](/docs/ADR/0001-docker-first-deployable-services.md).

#### Scenario: Construcción por separado

- **WHEN** la persona construye la imagen de producción de la web indicando la URL de la API
- **THEN** obtiene una imagen sin levantar Compose ni el resto de servicios

#### Scenario: Servir la web

- **WHEN** se ejecuta la imagen de producción y se abre su raíz o una ruta inexistente de la SPA
- **THEN** recibe la página de la web

#### Scenario: Imagen sin URL de la API

- **WHEN** se construye la imagen de producción sin indicar la URL de la API
- **THEN** la construcción falla e indica qué variable falta

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
