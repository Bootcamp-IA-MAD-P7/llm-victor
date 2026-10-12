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

[Hacia dónde va el producto y qué se construye primero, en dos o tres frases.]

## Hito 1 — [Resultado del hito]

### I1. [Iniciativa]

**Resultado:** [Qué cambia para el usuario o el equipo al completarla.]

#### I1-E1 — [Walking skeleton: camino mínimo de extremo a extremo] · Issue: pendiente

- **Resultado:** [Qué funciona de punta a punta, aunque sea mínimo.]
- **Requisitos:** RF-01
- **Depende de:** —

#### I1-E2 — [Capacidad de producto] · Issue: pendiente

- **Resultado:** [Capacidad acotada que funciona de extremo a extremo.]
- **Requisitos:** [RF-…]
- **Depende de:** I1-E1, porque [motivo]

## Orden entre iniciativas

| Iniciativa | Empieza cuando | Motivo |
|---|---|---|
| I1 | — | [Motivo] |
