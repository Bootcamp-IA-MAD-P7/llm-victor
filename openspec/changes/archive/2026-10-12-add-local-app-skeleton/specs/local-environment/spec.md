## Purpose

Arrancar y operar el sistema completo en local con un único punto de entrada, comprobar que sus servicios están sanos y ver desde la web si la API está disponible.

## ADDED Requirements

### Requirement: Arranque del sistema con un comando

El sistema SHALL arrancar la web, la API y la base vectorial con un único comando, y SHALL ofrecer comandos para detener, reiniciar, consultar el estado y ver los logs del conjunto.

Implementa: [ADR-0001](/docs/ADR/0001-docker-first-deployable-services.md); no hay RF directo.

#### Scenario: Arranque completo

- **WHEN** la persona ejecuta `make up` en un equipo con Docker y GNU Make
- **THEN** la web, la API y la base vectorial arrancan y llegan a estado sano

#### Scenario: Parada sin pérdida de datos

- **WHEN** la persona ejecuta `make down`
- **THEN** los tres servicios se detienen y los datos de la base vectorial se conservan

#### Scenario: Estado y logs

- **WHEN** la persona ejecuta `make ps` o `make logs`
- **THEN** ve el estado de cada servicio o sus logs

### Requirement: Salud de la API

La API SHALL exponer un endpoint de salud que indique si está disponible, según el [contrato de la API](/docs/CONTRACTS/api.md).

Implementa: [ADR-0001](/docs/ADR/0001-docker-first-deployable-services.md); no hay RF directo.

#### Scenario: API operativa

- **WHEN** se consulta el endpoint de salud y la API está en marcha
- **THEN** responde con éxito e indica que está disponible

### Requirement: Estado de la API visible en la web

La web SHALL indicar al usuario si la API está disponible y SHALL seguir funcionando cuando no lo está.

Relacionado: RNF-07.

#### Scenario: API disponible

- **WHEN** la persona abre la web y la API responde en su endpoint de salud
- **THEN** la web indica que la API está disponible

#### Scenario: API no disponible

- **WHEN** la persona abre la web y la API no responde
- **THEN** la web indica de forma comprensible que la API no está disponible, sin mostrar un error técnico ni quedarse en blanco

### Requirement: Configuración por entorno

Los servicios SHALL leer su configuración (puertos, URL de la API y orígenes permitidos) del entorno, con valores por defecto que permiten arrancar sin configuración previa; el repositorio SHALL NOT contener secretos.

Implementa: [ADR-0001](/docs/ADR/0001-docker-first-deployable-services.md); no hay RF directo.

#### Scenario: Arranque sin configuración

- **WHEN** no existe un archivo `.env` y la persona ejecuta `make up`
- **THEN** el sistema arranca con los valores por defecto

#### Scenario: Configuración propia

- **WHEN** la persona define en `.env` un puerto distinto para la web
- **THEN** la web queda accesible en ese puerto y sigue comunicándose con la API
