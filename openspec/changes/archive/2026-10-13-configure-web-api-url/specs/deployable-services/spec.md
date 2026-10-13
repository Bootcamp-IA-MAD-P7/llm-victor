## Purpose

Construir cada servicio de aplicación para desplegarlo por separado, configurado desde fuera y sin depender de direcciones locales, según ADR-0001.

## ADDED Requirements

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
