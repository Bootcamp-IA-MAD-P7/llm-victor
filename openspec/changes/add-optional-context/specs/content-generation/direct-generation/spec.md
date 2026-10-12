## ADDED Requirements

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
