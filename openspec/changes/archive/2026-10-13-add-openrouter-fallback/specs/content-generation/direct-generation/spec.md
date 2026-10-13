# content-generation/direct-generation

## ADDED Requirements

### Requirement: Recurrir a OpenRouter ante fallos elegibles de Groq (RNF-07)

Cuando Groq no está disponible o alcanza un límite o *rate limit*, el sistema SHALL recurrir una vez a OpenRouter para completar la generación. El fallback NO SHALL activarse por errores de validación de la solicitud ni por un modelo que el proveedor rechaza como no disponible. Si ambos proveedores fallan, el sistema SHALL devolver un error comprensible sin mostrar detalles internos.

#### Scenario: Indisponibilidad o límite de Groq activa el fallback

- **WHEN** Groq no responde, responde con un error de servidor o rechaza la petición por límite o *rate limit*
- **THEN** el sistema reintenta la generación con OpenRouter
- **THEN** el texto devuelto procede de OpenRouter

#### Scenario: La respuesta refleja el proveedor y el modelo efectivos tras el fallback

- **WHEN** la generación se completa con OpenRouter
- **THEN** la respuesta informa de `provider` y `model` con los valores efectivos de OpenRouter (RNF-03)
- **THEN** el modelo devuelto es el efectivo aunque difiera del modelo elegido

#### Scenario: Un error de validación de la solicitud no activa el fallback

- **WHEN** Groq rechaza la petición por un error de validación de la solicitud (por ejemplo, un parámetro no permitido)
- **THEN** el sistema NO recurre a OpenRouter
- **THEN** la API comunica el fallo de forma comprensible, sin detalles internos

#### Scenario: Un modelo no disponible no activa el fallback

- **WHEN** el modelo elegido estaba en el catálogo pero Groq lo rechaza como no disponible
- **THEN** el sistema NO recurre a OpenRouter
- **THEN** la API responde que el modelo ya no está disponible, como se define en «Comunicar un modelo no disponible»

#### Scenario: Si ambos proveedores fallan se comunica un error comprensible

- **WHEN** Groq falla con un error elegible y OpenRouter también falla
- **THEN** la API responde con un error de generación comprensible (RNF-07)
- **THEN** la respuesta no revela detalles internos ni secretos
- **THEN** el sistema no reintenta más allá de un intento de fallback
