# REQUIREMENTS

> Qué debe hacer el producto: requisitos con ID estable y criterios de aceptación de producto. Mapa de documentación: [WORKFLOW](../WORKFLOW.md#2-mapa-de-documentación).

<!--
- Este documento recoge la intención de producto, también la que todavía no está construida. El comportamiento implementado, con escenarios detallados, vive en openspec/specs/ y cita estos IDs.
- Aquí no van el alcance ni las exclusiones (PROJECT §6), el orden de entrega (ROADMAP) ni la tecnología (ARCHITECTURE).
- Un requisito describe un resultado observable y no elige tecnología.
- Los IDs no se reutilizan. Un requisito retirado se marca «Retirado» en lugar de borrarse.
-->

## 1. Glosario

| Término | Definición |
|---|---|
| Briefing | Tema o idea que el usuario quiere convertir en contenido, con las instrucciones que orientan el resultado |
| Configuración de generación | Opciones de una solicitud: plataforma, idioma, audiencia, tono, contexto, modelo y capacidades |
| Perfil del creador | Contexto reutilizable sobre la identidad profesional y las preferencias de comunicación del usuario; no es una fuente de hechos |
| Modalidad | Forma de generación que elige el usuario: directa, RAG o Graph RAG. La imagen es una capacidad complementaria |
| Generación directa | Generación con el briefing, la configuración y, si se indica, el perfil, sin recuperar conocimiento externo |
| RAG | Generación que usa información recuperada de documentos pertinentes de arXiv |
| Graph RAG | Evolución de RAG que además usa relaciones entre conceptos o documentos |
| Agente interno | Responsabilidad especializada del sistema (investigación, generación, imagen o evaluación) que el usuario no selecciona |

## 2. Flujos principales

1. Creador → introduce un briefing, elige idioma, audiencia, tono y modelo, y pide una publicación de LinkedIn → recibe un texto revisable.
2. Creador → crea o actualiza su perfil y pide una generación que lo use → recibe contenido personalizado.
3. Creador → elige generación basada en arXiv → recibe el contenido con las fuentes usadas.
4. Creador → elige Graph RAG → recibe contenido que aprovecha relaciones entre conceptos o documentos, con las fuentes disponibles.
5. Creador → pide una imagen asociada → la recibe junto al contenido.
6. Equipo → evalúa un resultado o compara configuraciones → obtiene criterios y observaciones.

## 3. Requisitos funcionales

**Ámbito:** Base, parte del primer producto utilizable · Evolución, ampliación prevista.

### RF-01 — Generar contenido desde un briefing

- **Objetivo:** OBJ-1
- **Ámbito:** Base

El sistema debe permitir solicitar contenido a partir de un briefing y devolver una pieza editable o utilizable para su revisión.

**Criterios de aceptación:**

- El usuario puede enviar un briefing no vacío.
- El sistema devuelve texto generado o comunica un error comprensible si no puede completarlo.
- El resultado corresponde al tema y las instrucciones del briefing.

### RF-02 — Configurar una generación

- **Objetivo:** OBJ-1
- **Ámbito:** Base

El usuario debe poder especificar la plataforma, la audiencia, el idioma, el tono y el contexto adicional de una generación, y el sistema debe aplicarlos al resultado.

**Criterios de aceptación:**

- La interfaz permite consultar y cambiar esas opciones antes de generar.
- El idioma seleccionado determina el idioma del contenido devuelto.
- El resultado tiene en cuenta la audiencia, el tono y el contexto especificados.
- La plataforma inicial disponible es LinkedIn.

### RF-03 — Generar contenido adaptado a LinkedIn

- **Objetivo:** OBJ-1
- **Ámbito:** Base

El sistema debe adaptar la pieza al uso en LinkedIn y al propósito comunicativo descrito por el usuario.

**Criterios de aceptación:**

- El contenido es una publicación lista para revisar antes de copiarla o utilizarla.
- El sistema no publica el contenido en LinkedIn.
- Las restricciones de longitud o formato se aplican cuando forman parte de la configuración o de las reglas de producto acordadas.

### RF-04 — Seleccionar un idioma

- **Objetivo:** OBJ-1
- **Ámbito:** Base

El usuario debe poder elegir español, inglés, francés o italiano como idioma de salida.

**Criterios de aceptación:**

- Las cuatro opciones están disponibles para la generación de texto.
- El resultado se produce en el idioma seleccionado.

### RF-05 — Seleccionar un modelo disponible

- **Objetivo:** OBJ-1
- **Ámbito:** Base

El usuario debe poder elegir entre las opciones de modelo disponibles para la tarea. Elegir no implica comparar modelos automáticamente ni generar varias respuestas.

**Criterios de aceptación:**

- El usuario puede ver y elegir las opciones ofrecidas para la tarea.
- La generación utiliza la opción seleccionada.
- Si una opción deja de estar disponible, el sistema lo comunica y permite elegir otra.

### RF-06 — Mantener el perfil del creador

- **Objetivo:** OBJ-2
- **Ámbito:** Evolución

El sistema debe permitir definir y actualizar un perfil con información profesional y preferencias pertinentes: nombre, profesión, experiencia, especialidades, intereses, audiencia habitual, estilo de comunicación e información adicional. En la primera versión, el perfil persiste en el navegador del usuario; la sincronización entre dispositivos queda para más adelante.

**Criterios de aceptación:**

- El usuario puede crear, consultar y modificar su perfil.
- El perfil se conserva al recargar la aplicación en el mismo navegador y origen.
- Los campos no proporcionados no se inventan ni se presentan como hechos del perfil.
- El usuario puede pedir que el perfil se use en una generación.

### RF-07 — Personalizar con el perfil

- **Objetivo:** OBJ-2
- **Ámbito:** Evolución

Cuando el usuario lo pida, el sistema debe usar el perfil como contexto para adaptar el contenido, sin presentarlo como fuente externa de hechos.

**Criterios de aceptación:**

- La generación tiene en cuenta las preferencias y la información pertinente del perfil.
- El usuario puede generar contenido sin aplicar el perfil.
- La información del perfil no sustituye ni se confunde con las fuentes científicas de RAG.

### RF-08 — Solicitar una imagen asociada

- **Objetivo:** OBJ-3
- **Ámbito:** Evolución

El usuario debe poder solicitar opcionalmente una imagen relacionada con el contenido generado.

**Criterios de aceptación:**

- La imagen es una opción que el usuario activa o deja desactivada.
- Si se solicita y el servicio está disponible, el sistema devuelve la imagen o un resultado accesible junto al contenido.
- Si la imagen no se puede generar, el sistema lo comunica sin ocultar ni perder el texto.

### RF-09 — Recuperar conocimiento de arXiv con RAG

- **Objetivo:** OBJ-4
- **Ámbito:** Evolución

El sistema debe poder recuperar documentos de arXiv pertinentes para una solicitud y usar su contenido como contexto en una generación elegida por el usuario.

**Criterios de aceptación:**

- El flujo RAG se distingue de la generación directa y el usuario puede solicitarlo.
- El resultado se basa en los documentos recuperados pertinentes y no presenta una generación directa como fundamentada en ellos.
- Si no hay fuentes pertinentes o la recuperación falla, el sistema lo comunica y no atribuye un respaldo documental inexistente.

### RF-10 — Mostrar las fuentes de RAG

- **Objetivo:** OBJ-4
- **Ámbito:** Evolución

En las generaciones con RAG, el sistema debe identificar las fuentes de arXiv usadas de forma que el usuario pueda reconocer y consultar los documentos.

**Criterios de aceptación:**

- Las fuentes presentadas corresponden a documentos realmente recuperados para esa generación.
- Se muestra información suficiente para identificar y localizar cada documento, con su identificador o enlace.
- Las fuentes se mantienen asociadas al resultado generado.

### RF-11 — Utilizar Graph RAG

- **Objetivo:** OBJ-4
- **Ámbito:** Evolución

El sistema debe poder usar relaciones entre conceptos y documentos, además de la recuperación de documentos, para producir contenido en el flujo Graph RAG.

**Criterios de aceptación:**

- Graph RAG se ofrece como una modalidad diferenciada de RAG.
- El resultado puede apoyarse tanto en documentos como en relaciones pertinentes.
- Las fuentes documentales usadas se muestran cuando están disponibles.
- Si las relaciones no aportan contexto pertinente, el sistema no afirma que el resultado se basa en una conexión inexistente.

### RF-12 — Separar responsabilidades mediante agentes internos

- **Objetivo:** OBJ-5
- **Ámbito:** Evolución

El sistema puede usar agentes internos para responsabilidades como investigación, generación, imagen o evaluación. El usuario elige la capacidad o el flujo, nunca los agentes que lo ejecutan.

**Criterios de aceptación:**

- Las responsabilidades internas corresponden a tareas identificables del flujo.
- El usuario elige la modalidad o capacidad, no el nombre ni la implementación del agente.
- El modelo es una opción de ejecución y no determina la identidad del agente.

### RF-13 — Elegir explícitamente el flujo

- **Objetivo:** OBJ-1
- **Ámbito:** Evolución

El usuario debe poder elegir las capacidades que aplica (generación directa, RAG, Graph RAG o imagen) sin depender de una selección automática obligatoria.

**Criterios de aceptación:**

- La generación directa puede usarse sin RAG ni imagen.
- RAG y Graph RAG se presentan diferenciadas cuando están disponibles.
- La imagen puede solicitarse como capacidad complementaria cuando está disponible.
- El sistema respeta la modalidad elegida y comunica cuándo una capacidad aún no está disponible.

### RF-14 — Evaluar resultados con herramientas internas

- **Objetivo:** OBJ-6
- **Ámbito:** Evolución

El equipo debe poder evaluar generaciones con criterios definidos de adecuación al briefing, audiencia, tono, coherencia y, cuando corresponda, apoyo en fuentes. Es una herramienta interna, no parte de la interfaz inicial para creadores.

**Criterios de aceptación:**

- La evaluación identifica los criterios aplicados y las observaciones relevantes.
- La evaluación no se presenta como garantía de corrección factual.
- Los resultados de evaluación pueden asociarse a la generación revisada.

### RF-15 — Aplicar guardrails

- **Objetivo:** OBJ-6
- **Ámbito:** Evolución

El sistema debe aplicar controles que detecten o reduzcan resultados que contradigan las instrucciones, excedan las restricciones configuradas o, en un flujo con conocimiento, presenten como respaldadas afirmaciones sin fuentes suficientes.

**Criterios de aceptación:**

- Los controles se aplican antes de presentar como final una salida que infrinja restricciones definidas.
- Según el caso, el sistema señala el problema, lo corrige o pide la intervención del usuario.
- Los controles no se describen como eliminación total de errores o alucinaciones.

### RF-16 — Comparar configuraciones mediante benchmark

- **Objetivo:** OBJ-6
- **Ámbito:** Evolución

El equipo debe poder comparar resultados de configuraciones distintas (prompts, modelos o flujos) con un conjunto de casos y criterios definidos. Es una herramienta de experimentación, no parte de la interfaz inicial para creadores.

**Criterios de aceptación:**

- Cada resultado de comparación se asocia a la configuración utilizada.
- Los criterios y casos empleados se pueden identificar.
- La comparación sirve para revisar resultados; no obliga al usuario final a generar con varios modelos a la vez.

### RF-17 — Añadir orquestación opcional

- **Objetivo:** OBJ-5
- **Ámbito:** Evolución

El sistema podrá recomendar o seleccionar automáticamente un flujo y sus agentes. Esta capacidad es opcional y no elimina los flujos explícitos.

**Criterios de aceptación:**

- El usuario puede seguir eligiendo el flujo explícitamente cuando la orquestación esté disponible.
- El sistema no activa capacidades en silencio en contra de la preferencia del usuario.

## 4. Requisitos no funcionales

### RNF-01 — Usabilidad

El flujo de briefing, configuración, generación y revisión se completa sin conocer conceptos internos como agentes, embeddings o grafos.

**Criterios de aceptación:**

- Las opciones se presentan como capacidades que el usuario puede elegir, con explicaciones suficientes para diferenciarlas.

### RNF-02 — Control del usuario

El usuario revisa las opciones relevantes antes de generar y decide si usa perfil, conocimiento externo e imagen. El sistema comunica las limitaciones que impidan respetar una elección.

### RNF-03 — Trazabilidad

Durante una sesión, cada resultado se asocia a la configuración usada; en RAG y Graph RAG, también a las fuentes disponibles, y en flujos evaluados, a los criterios y resultados de la evaluación. La versión inicial no persiste generaciones ni metadatos entre sesiones.

### RNF-04 — Reproducibilidad y comparación

Cuando se incorpore la persistencia de generaciones, el sistema conservará lo necesario para analizar una generación y comparar configuraciones: briefing, idioma, audiencia, tono, modelo, modalidad y, cuando correspondan, fuentes. Esa persistencia no forma parte del alcance inicial.

### RNF-05 — Extensibilidad

El producto puede evolucionar hacia otras plataformas, dominios, modelos, fuentes, flujos y agentes sin que el usuario tenga que conocer los detalles internos de cada integración.

### RNF-06 — Coste

Se priorizan alternativas gratuitas, locales o de bajo coste cuando son adecuadas, y el producto se puede demostrar dentro de las limitaciones económicas del POC. No hay presupuesto numérico hasta conocer las opciones de modelo y ejecución.

### RNF-07 — Disponibilidad y fallos externos

La indisponibilidad de un modelo, del servicio de imagen o de una fuente externa se comunica de forma comprensible. El fallo de una capacidad opcional no oculta un texto ya generado.

### RNF-08 — Calidad evaluable

El producto permite analizar la adecuación al briefing, idioma, audiencia y tono, y evolucionar hacia la evaluación de factualidad y la comparación de estrategias. No hay umbral universal de calidad hasta definir el método de evaluación.

## 5. Reglas de dominio

- **RD-01:** el dominio inicial del contenido es la inteligencia artificial.
- **RD-02:** la plataforma inicial de destino es LinkedIn.
- **RD-03:** arXiv es la fuente científica inicial y única del conocimiento externo.
- **RD-04:** el sistema distingue claramente la generación directa de la que usa conocimiento recuperado.
- **RD-05:** las afirmaciones presentadas como respaldadas se pueden relacionar con las fuentes usadas cuando están disponibles.
- **RD-06:** el perfil del creador expresa contexto y preferencias del usuario; no es fuente científica ni evidencia externa.
- **RD-07:** el control explícito del usuario sobre las modalidades tiene prioridad sobre la automatización.
