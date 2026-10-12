# ROADMAP

> En qué orden se construye el producto: hitos, iniciativas, épicas y dependencias entre ellas. Mapa de documentación: [WORKFLOW](../WORKFLOW.md#2-mapa-de-documentación).

<!--
- Iniciativas y épicas se dividen en vertical slices: capacidades que funcionan de extremo a extremo, no capas técnicas. La primera épica es un walking skeleton (WORKFLOW §5).
- El ROADMAP llega hasta las épicas. Las historias, sus tareas, el estado y los bloqueos concretos viven en GitHub.
- Aquí no van el alcance (PROJECT §6) ni los requisitos (REQUIREMENTS).
- No se ponen fechas salvo por decisión expresa.
- Los IDs de planificación (I1 para iniciativas, I1-E1 para épicas) no son números de Issue. Al crear la Issue de una épica se añade su enlace.
-->

## Dirección

Primero, un flujo sencillo y controlable que convierta un briefing en una publicación de LinkedIn sobre IA, ejecutado en local con Docker desde el primer día. Después, ampliarlo con perfil, imagen y conocimiento de arXiv (RAG y Graph RAG), guardrails y evaluación y, cuando aporten una mejora medible, agentes y orquestación opcional.

## Hito 1 — Base local y generación directa

### I1. Aplicación local para generar contenido de LinkedIn

**Resultado:** una aplicación local, operada con Docker Compose y Makefile, genera y deja revisar una publicación de LinkedIn desde un briefing con audiencia, tono, contexto, idioma y modelo. La web y la API quedan listas para construirse y configurarse por separado, sin desplegar en producción.

#### I1-E1 — Walking skeleton: publicación desde un briefing · Issue: pendiente

- **Resultado:** desde la web se envía un briefing, la API genera el texto con Groq y la web lo muestra; un briefing vacío o un fallo de generación se comunican de forma comprensible, sin perder el formulario. La web, la API y Qdrant arrancan con Docker Compose y se operan con el Makefile (comandos globales y por servicio). La configuración va por entorno, sin secretos, y el CI ejecuta los checks del stack.
- **Requisitos:** RF-01, RF-03
- **Depende de:** —

#### I1-E2 — Configurar audiencia, tono y contexto · Issue: pendiente

- **Resultado:** el usuario elige audiencia y tono y añade contexto opcional antes de generar; esos valores llegan a la API y se reflejan en el texto, sin que el contexto se confunda con las instrucciones del sistema.
- **Requisitos:** RF-02
- **Depende de:** I1-E1, porque amplía su formulario y su contrato.

#### I1-E3 — Generar en cuatro idiomas · Issue: pendiente

- **Resultado:** cada generación se puede pedir en español (valor inicial), inglés, francés o italiano y llega en ese idioma; las opciones no válidas se rechazan.
- **Requisitos:** RF-04
- **Depende de:** I1-E1, porque amplía su formulario y su contrato.

#### I1-E4 — Elegir un modelo disponible · Issue: pendiente

- **Resultado:** la API expone un catálogo de modelos de texto con identificadores estables y sin secretos; el usuario elige uno, la API lo valida y lo usa, y avisa si deja de estar disponible.
- **Requisitos:** RF-05
- **Depende de:** I1-E1, porque amplía su formulario y su contrato.

#### I1-E5 — Fallback de proveedor y trazabilidad · Issue: pendiente

- **Resultado:** si Groq no está disponible o alcanza un límite, la API recurre a OpenRouter (nunca ante errores de validación), y la respuesta y la web muestran el proveedor y el modelo efectivos.
- **Requisitos:** RNF-03, RNF-07
- **Depende de:** I1-E4, porque la selección explícita debe existir antes del fallback para conservar la trazabilidad.

#### I1-E6 — Servicios desplegables por separado · Issue: pendiente

- **Resultado:** las imágenes de la web y de la API se construyen por separado y se conectan a una API y a un Qdrant externos solo por configuración (URL de la API, CORS y secretos); queda documentado lo necesario para un hosting futuro, sin desplegar.
- **Requisitos:** RNF-05; [ADR-0001](ADR/0001-docker-first-deployable-services.md)
- **Depende de:** I1-E1. No bloquea el resto de I1.

## Hito 2 — Personalización e imagen opcional

### I2. Personalizar el contenido con el perfil del creador

**Resultado:** el usuario guarda un perfil local y decide en cada generación si lo aporta como contexto.

#### I2-E1 — Crear y guardar el perfil en el navegador · Issue: pendiente

- **Resultado:** el usuario crea, consulta y edita su perfil con los campos acordados; se guarda en `localStorage` y los datos ausentes o incompatibles no se inventan.
- **Requisitos:** RF-06
- **Depende de:** I1-E1, porque el perfil se integra en la web existente.

#### I2-E2 — Aplicar el perfil a una generación · Issue: pendiente

- **Resultado:** el usuario activa o desactiva el perfil en cada generación; la API lo usa como contexto de estilo, nunca como fuente científica, y la web indica que se aplicó.
- **Requisitos:** RF-07, RD-06
- **Depende de:** I2-E1, porque necesita un perfil guardado.

### I3. Generar una imagen opcional

**Resultado:** el usuario puede pedir una imagen complementaria y, si falla, conserva el texto.

#### I3-E1 — Imagen opcional junto al texto · Issue: pendiente

- **Resultado:** primero se verifica que Cloudflare Workers AI se puede usar sin datos de pago ni facturación (alta, cuota y límites) y se decide seguir, cambiar de proveedor o pausar. Si se sigue, la API genera la imagen solo cuando se pide y la web la muestra; si falla o se agota la cuota, el texto se mantiene.
- **Requisitos:** RF-08, RNF-07
- **Depende de:** I1-E1, porque la imagen acompaña al texto generado. Sin un proveedor viable sin facturación, se pausa y se revisa el alcance.

## Hito 3 — Conocimiento científico con RAG

### I4. Fundamentar las generaciones con artículos de arXiv

**Resultado:** el usuario elige RAG de forma explícita y recibe contenido basado en documentos pertinentes, con fuentes identificables.

#### I4-E1 — RAG sobre un corpus inicial de arXiv · Issue: pendiente

- **Resultado:** un manifiesto versionado con un corpus acotado se ingiere con un comando (descarga de los documentos permitidos, extracción, fragmentos con su atribución y embeddings locales con el modelo candidato) en una colección de Qdrant. El usuario elige RAG, la generación usa los fragmentos recuperados y la web muestra las fuentes, o avisa si no hay ninguna pertinente o la recuperación falla.
- **Requisitos:** RF-09, RF-10, RF-13, RD-03, RD-04, RD-05
- **Depende de:** I1-E1, porque amplía la generación directa y usa el Qdrant del entorno local.

#### I4-E2 — Elegir el modelo de embeddings con evidencia · Issue: pendiente

- **Resultado:** BGE-M3 y otros candidatos multilingües se comparan con un conjunto pequeño de consultas según calidad, recursos locales, licencia y compatibilidad; el modelo y la dimensión elegidos se registran en un ADR y la colección se reconstruye sin mezclar vectores incompatibles.
- **Requisitos:** RF-09
- **Depende de:** I4-E1, porque compara sobre el flujo RAG ya funcionando.

#### I4-E3 — Corpus definitivo y reingesta reproducible · Issue: pendiente

- **Resultado:** el corpus sigue criterios acordados (tema, idioma, antigüedad, inclusión y exclusión) y se puebla o reconstruye desde el manifiesto de forma repetible, tratando los documentos no disponibles.
- **Requisitos:** RF-09, RD-03
- **Depende de:** I4-E2, porque el corpus definitivo se indexa con el modelo elegido.

## Hito 4 — Graph RAG

### I5. Incorporar relaciones entre artículos y conceptos

**Resultado:** el usuario puede elegir Graph RAG como modalidad diferenciada de RAG y revisar los documentos y las relaciones utilizados.

#### I5-E1 — Graph RAG con citas entre artículos · Issue: pendiente

- **Resultado:** se modelan las citas entre artículos con su procedencia y se elige el almacenamiento de grafo en un ADR antes de implementarlo. Las relaciones se construyen desde el corpus RAG; el usuario elige Graph RAG, la generación combina relaciones y fragmentos, y la web muestra fuentes y procedencia sin atribuir conexiones no recuperadas.
- **Requisitos:** RF-11, RF-13, RD-05
- **Depende de:** I4-E3, porque el grafo se construye sobre el corpus definitivo.

#### I5-E2 — Conceptos compartidos en el grafo · Issue: pendiente

- **Resultado:** el grafo incorpora conceptos extraídos y normalizados de los artículos, si la técnica elegida lo permite, y Graph RAG los usa con su procedencia.
- **Requisitos:** RF-11
- **Depende de:** I5-E1, porque amplía su grafo.

## Hito 5 — Calidad, guardrails y evaluación

### I6. Aplicar guardrails en los flujos que los necesitan

**Resultado:** el sistema comprueba restricciones acordadas y trata los incumplimientos antes de presentar una salida como final, sin prometer que elimina los errores. Los guardrails se añaden por flujo, no como una capa que bloquee toda la funcionalidad.

#### I6-E1 — Restricciones en la generación directa · Issue: pendiente

- **Resultado:** se acuerdan restricciones comprobables de formato, tono o longitud; el sistema las valida antes de presentar el resultado, señala los incumplimientos y ofrece las acciones disponibles.
- **Requisitos:** RF-15
- **Depende de:** I1-E1, porque controla su salida.

#### I6-E2 — Afirmaciones sin apoyo en flujos con fuentes · Issue: pendiente

- **Resultado:** en RAG y Graph RAG, el sistema detecta y comunica las afirmaciones sin apoyo suficiente en las fuentes realmente recuperadas, según criterios acordados.
- **Requisitos:** RF-15, RD-05
- **Depende de:** I4-E1, porque necesita fuentes recuperadas; se amplía a Graph RAG con I5-E1.

### I7. Evaluar resultados y comparar configuraciones

**Resultado:** el equipo ejecuta casos reproducibles y compara generaciones, prompts, modelos o modalidades.

#### I7-E1 — Evaluar y comparar la generación directa · Issue: pendiente

- **Resultado:** un conjunto acotado de casos y una rúbrica revisable (adecuación al briefing, audiencia, idioma, tono y coherencia) se ejecutan de forma reproducible, registrando la configuración en un formato local sin persistencia de producto, y permiten comparar dos o más configuraciones con un resumen para revisión.
- **Requisitos:** RF-14, RF-16, RNF-08
- **Depende de:** I1-E1, porque evalúa su salida.

#### I7-E2 — Evaluar los flujos con fuentes · Issue: pendiente

- **Resultado:** los casos comprueban referencias, atribución y uso de evidencia en RAG y, después, en Graph RAG.
- **Requisitos:** RF-14, RD-05
- **Depende de:** I7-E1 e I4-E1; se amplía con I5-E1.

## Hito 6 — Agentes internos y orquestación opcional

### I8. Incorporar agentes especializados cuando mejoren un flujo

**Resultado:** el sistema separa una responsabilidad interna solo si mejora un resultado observable; el usuario sigue eligiendo capacidades, no agentes.

#### I8-E1 — Primer agente especializado · Issue: pendiente

- **Resultado:** se elige una responsabilidad concreta con un beneficio medible y criterios de comparación frente al flujo actual. Si la medición lo justifica, se implementa con LangGraph dentro de una modalidad existente, sin exponer el agente, y se compara con la línea base de evaluación.
- **Requisitos:** RF-12
- **Depende de:** I7-E1, porque necesita la línea base. Si no se demuestra una mejora, no se integra.

### I9. Ofrecer orquestación automática opcional

**Resultado:** el usuario puede activar recomendaciones o la selección automática de flujos sin perder la elección explícita.

#### I9-E1 — Recomendar una modalidad · Issue: pendiente

- **Resultado:** con criterios de selección y casos de evaluación definidos, el sistema recomienda una modalidad y explica por qué; el usuario la acepta o elige otra, y nada se activa en silencio.
- **Requisitos:** RF-17, RD-07
- **Depende de:** modalidades explícitas estables (I1, I4 o I5, e I3 si aplica) y los casos de I7.

#### I9-E2 — Selección automática opcional · Issue: pendiente

- **Resultado:** si el usuario la activa, el sistema elige y ejecuta la modalidad, informa de cuál y por qué, y mantiene la ruta explícita.
- **Requisitos:** RF-17, RD-07
- **Depende de:** I9-E1.

## Orden entre iniciativas

| Iniciativa | Empieza cuando | Motivo |
|---|---|---|
| I1 | — | Base del producto |
| I2 | I1-E1 | El perfil se aplica sobre la generación directa |
| I3 | I1-E1 | La imagen acompaña al texto generado |
| I4 | I1-E1 | RAG amplía la generación directa y usa el Qdrant local |
| I5 | I4 | Graph RAG evoluciona RAG sobre su corpus |
| I6 | I1-E1 (E1) · I4-E1 (E2) | Los guardrails se añaden por flujo |
| I7 | I1-E1 | La generación directa es la línea base |
| I8 | I7-E1 | Un agente solo se integra si mejora un flujo medible |
| I9 | I1, I4 o I5, e I7 | La orquestación elige entre flujos explícitos ya estables; I8 no es requisito |
