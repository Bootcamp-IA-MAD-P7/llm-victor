# PROJECT

> Por qué existe el producto, para quién y hasta dónde llega. Mapa de documentación: [WORKFLOW](../WORKFLOW.md#2-mapa-de-documentación).

- **Nombre:** AI Content Studio
- **Responsable:** Glezino
- **Estado del documento:** Aprobado

<!--
Las secciones crecen cuando se toman decisiones. Lo no confirmado va a «Preguntas abiertas».
Aquí no van requisitos detallados (REQUIREMENTS), decisiones técnicas (ARCHITECTURE y ADR), orden de trabajo (ROADMAP) ni estado (GitHub).
-->

## 1. Resumen

AI Content Studio es una plataforma web que convierte el briefing de un creador en contenido profesional adaptado a su audiencia, idioma, tono y plataforma, con el usuario en control de cómo se genera. Empieza con publicaciones de LinkedIn sobre inteligencia artificial y evoluciona hacia personalización, imágenes, conocimiento científico de arXiv (RAG y Graph RAG), agentes especializados y evaluación. Nace como POC de un ejercicio práctico de IA generativa: demostrar, en un único producto coherente, la evolución desde la generación con prompts hasta flujos con conocimiento, agentes, guardrails y evaluación.

## 2. Problema y oportunidad

- **Problema:** crear contenido de calidad exige combinar conocimiento del tema, redacción, adaptación al canal y al tono y, a veces, información especializada. Las herramientas genéricas generan texto rápido, pero con poca personalización y control del proceso, sin acceso estructurado a conocimiento especializado, sin transparencia sobre las fuentes y sin forma sistemática de evaluar la calidad: el resultado suele parecer una generación genérica.
- **Oportunidad:** un estudio de creación de contenido inteligente y controlable, que reduzca el esfuerzo de pasar de una idea a una pieza utilizable sin quitar el control al usuario, e incorpore de forma progresiva personalización, distintos modelos, imágenes, RAG, Graph RAG, agentes, evaluación y guardrails.

## 3. Usuarios y partes interesadas

- **Usuarios:** creadores y profesionales que publican sobre IA, sobre todo en LinkedIn: profesionales de tecnología, desarrolladores, especialistas en IA, consultores, divulgadores y quien construye su marca personal. Necesitan rapidez, calidad, control y personalización. La versión inicial se dirige a un único usuario principal.
- **Partes interesadas:**
  - Propietario y desarrollador: necesita una solución extensible para experimentar con modelos y estrategias sin complicar la experiencia.
  - Evaluadores del proyecto o del curso: necesitan comprobar que LLM, RAG, Graph RAG, agentes, evaluación y guardrails se aplican de forma real y coherente.
  - Usuarios de prueba y personas interesadas en aplicaciones prácticas de LLM.

## 4. Objetivos y criterios de éxito

<!-- Cada objetivo tiene un ID estable que citan los requisitos y una forma observable de comprobarlo. -->

| ID | Objetivo | Cómo se comprueba |
|---|---|---|
| OBJ-1 | Generar una publicación de LinkedIn sobre IA desde un briefing, adaptada al idioma, la audiencia, el tono y el modelo que elige el usuario | Desde un briefing se obtiene contenido útil en los cuatro idiomas, adaptado a la audiencia y al tono; tasa de generaciones satisfactorias según evaluación humana |
| OBJ-2 | Personalizar el contenido con el perfil del creador | El perfil cambia la generación de forma apreciable y el resultado es coherente con él |
| OBJ-3 | Acompañar el contenido con una imagen opcional | Se genera una imagen asociada; si falla, el texto se conserva |
| OBJ-4 | Fundamentar el contenido en artículos de arXiv con RAG y evolucionarlo a Graph RAG | Las generaciones muestran sus fuentes; menos información incorrecta; diferencia de calidad y factualidad entre generación directa, RAG y Graph RAG |
| OBJ-5 | Separar responsabilidades internas con agentes especializados, sin que el usuario tenga que elegirlos | Hay agentes con responsabilidades diferenciadas que mejoran un flujo frente a su línea base |
| OBJ-6 | Evaluar la calidad, aplicar guardrails y comparar configuraciones | Los resultados se evalúan y se pueden trazar; porcentaje que supera los guardrails; comparación de modelos y configuraciones; tiempo y coste aproximados por generación |

**Éxito global:** demostrar que las capacidades avanzadas no son funcionalidades aisladas, sino la evolución lógica de un mismo producto.

## 5. Principios de decisión

1. **Control del usuario:** el usuario elige capacidades y modelos; la automatización no le quita esa decisión.
2. **Calidad y utilidad** del contenido generado.
3. **Coherencia del producto:** cada extensión se valora por su encaje con el foco IA + LinkedIn.
4. **Capacidad de evolución y experimentación.**
5. **Simplicidad de uso:** la experiencia es briefing → configuración → generación → resultado; agentes, recuperación y evaluación quedan dentro del sistema.

Ante un conflicto entre añadir una capacidad y mantener una experiencia clara y controlable, se prioriza lo segundo.

## 6. Alcance

### Incluido

- Interfaz web para crear contenido y revisar resultados.
- Publicaciones de LinkedIn sobre IA desde un briefing, con audiencia, tono, contexto e idioma (español, inglés, francés e italiano).
- Selección entre los modelos de texto disponibles.
- Perfil del creador para personalizar las generaciones.
- Imagen opcional asociada al contenido.
- RAG sobre artículos de arXiv y Graph RAG como su evolución.
- Agentes internos especializados.
- Guardrails, evaluación de resultados y benchmark para comparar configuraciones.
- Orquestación automática opcional, como última evolución y sin eliminar la elección explícita (DEC-07).

### Fuera de alcance

- Publicación automática en LinkedIn u otras redes, gestión de cuentas, campañas, calendarios editoriales y analítica social: el producto crea contenido, no lo publica (DEC-08).
- Un producto completo de marketing o *social media management*.
- Multiusuario, organizaciones, autenticación y gestión avanzada de cuentas: el POC se dirige a un único usuario.
- Fuentes científicas distintas de arXiv y dominios distintos de IA en la primera versión (DEC-02, DEC-03).
- Noticias financieras y análisis de mercados, por falta de encaje con el producto (DEC-10).
- Despliegue en producción y persistencia central del perfil o del historial de generaciones.
- Agentes de programación o herramientas de desarrollo: los agentes del producto son internos al flujo de contenido.

### Futuro

<!-- Ideas sin compromiso. Solo pasan a «Incluido» con una decisión explícita. -->

- Otras plataformas (X/Twitter, Instagram) y otros dominios además de IA.
- Otras fuentes de conocimiento y documentos aportados por el usuario.
- Más agentes especializados.
- Personalización avanzada del estilo y memoria de preferencias y contexto del usuario.
- Evaluación automática más sofisticada, métricas avanzadas y comparación sistemática entre modelos.
- Persistencia del perfil y del historial, con sincronización entre dispositivos.
- Integración con plataformas de publicación, si el producto lo requiriese.
- Una capacidad informativa centrada en IA, como extensión independiente.

## 7. Restricciones, supuestos y riesgos

- **Restricciones:**
  - POC de alcance razonable y recursos económicos limitados: se priorizan modelos locales, servicios gratuitos o planes de prueba.
  - Los modelos y servicios externos pueden tener límites de velocidad, cuota o disponibilidad.
  - Foco inicial en LinkedIn e inteligencia artificial, con arXiv como única fuente científica.
  - Debe poder demostrarse en un entorno de desarrollo y presentación.
- **Supuestos:**
  - Los usuarios aportan contexto suficiente para orientar la generación.
  - Los modelos disponibles bastan para los casos de uso elegidos.
  - arXiv aporta volumen suficiente para demostrar RAG y Graph RAG.
  - La generación no sustituye el criterio del usuario.
  - Cada capacidad avanzada se construye sobre las anteriores.
- **Dependencias:** disponibilidad, calidad y límites de los modelos de lenguaje, de los servicios de imagen y del acceso a arXiv.
- **Riesgos:**
  - Alucinaciones, sobre todo en temas científicos → RAG, referencias a fuentes, evaluación y guardrails.
  - Complejidad creciente con agentes, RAG y Graph RAG → evolución incremental y separación clara entre capacidades.
  - Coste del uso intensivo de modelos externos → modelos locales, gratuitos o de bajo coste.
  - Pérdida de control por una orquestación demasiado automática → flujos explícitos primero; orquestación opcional.
  - Falta de coherencia, convertirse en una colección de demos desconectadas → mantener el foco IA + LinkedIn y valorar cada extensión por su encaje.

## 8. Decisiones de producto

<!-- Una decisión no se reescribe: se marca como reemplazada y se añade la nueva. Las técnicas van en docs/ADR/. -->

| ID | Decisión | Motivo | Estado |
|---|---|---|---|
| DEC-01 | Empezar centrados en LinkedIn | Caso de uso concreto y coherente que no impide añadir otras plataformas | Aceptada |
| DEC-02 | Especializar el contenido inicial en inteligencia artificial | Identidad de producto clara, conectada con el conocimiento científico de arXiv | Aceptada |
| DEC-03 | arXiv como única fuente científica de la primera versión | Reduce la complejidad del POC y permite demostrar RAG y Graph RAG con una fuente amplia y relevante | Aceptada |
| DEC-04 | Graph RAG es una evolución de RAG, no una capacidad independiente | Ambas pertenecen al mismo ámbito de conocimiento; Graph RAG añade relaciones estructuradas | Aceptada |
| DEC-05 | El usuario elige explícitamente generación directa, RAG, Graph RAG o imagen | Prioriza el control y la experimentación frente a una automatización que tome decisiones no deseadas | Aceptada |
| DEC-06 | Los agentes son internos; el usuario no los selecciona | El usuario elige qué capacidad usar, no la implementación que la ejecuta | Aceptada |
| DEC-07 | La orquestación automática llega después y no es el comportamiento inicial | Primero capacidades deterministas y controlables; la orquestación es una capa posterior | Aceptada |
| DEC-08 | Generar contenido, no publicarlo | Mantiene el alcance controlado y centrado en la IA generativa | Aceptada |
| DEC-09 | Personalizar con un perfil del creador | Demuestra personalización real sin la complejidad de una plataforma multiusuario | Aceptada |
| DEC-10 | Excluir el dominio financiero del núcleo | No encaja con el foco; cualquier capacidad informativa futura se valorará por su coherencia con IA | Aceptada |

## 9. Preguntas abiertas

<!-- Una pregunta resuelta se convierte en decisión, requisito o alcance, y se borra de aquí. -->

- ¿Qué elementos exactos debe incluir el briefing mínimo? Bloquea: I1-E1.
- ¿Debe haber un campo explícito de objetivo comunicativo o basta con el contexto? Bloquea: I1-E2.
- ¿Qué configuración se ofrece a un usuario básico frente a uno avanzado? Bloquea: I1-E2.
- ¿Cómo se explica al usuario la diferencia entre generación directa, RAG y Graph RAG? Bloquea: I4-E1.
- ¿Cómo se presentan las fuentes al usuario? Bloquea: I4-E1.
- ¿Qué subconjunto de arXiv forma el corpus inicial? Bloquea: I4-E1.
- ¿Con qué criterios se seleccionan y actualizan los documentos del corpus? Bloquea: I4-E3.
- ¿Qué entidades y relaciones concretas de citas y conceptos compartidos se modelan en el grafo? Bloquea: I5-E1.
- ¿Qué características definen el estilo personalizado del creador? Bloquea: I2-E1.
- ¿Cómo se tratan los artículos frente a las publicaciones de LinkedIn sin crear una jerarquía innecesaria de tipos de contenido? Bloquea: la ampliación a otros formatos.
- ¿Qué criterios determinan que una generación es lo bastante buena para darla por final? Bloquea: I7-E1.
- ¿Qué métricas son lo bastante objetivas para comparar generaciones y qué parte de la evaluación es automática o humana? Bloquea: I7-E1.
- ¿Cómo se construye un benchmark representativo? Bloquea: I7-E1.
- ¿Cómo se mide la reducción de alucinaciones? Bloquea: I6-E2 e I7-E2.
- ¿Qué responsabilidades merecen un agente independiente y cuándo aporta valor frente a una cadena única? Bloquea: I8-E1.
- ¿Qué criterios guían al futuro orquestador? Bloquea: I9-E1.
