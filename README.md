# AI Content Studio

Plataforma web que convierte un briefing en contenido profesional para LinkedIn sobre inteligencia artificial, con el usuario en control de cómo se genera. Más contexto en [`docs/PROJECT.md`](docs/PROJECT.md).

## Estado

El trabajo se sigue en [GitHub Issues](https://github.com/Glezino/ai-content-generator/issues) y las versiones se publican en [Releases](https://github.com/Glezino/ai-content-generator/releases).

## Puesta en marcha

<!-- Requisitos y los dos o tres comandos para arrancar. El detalle operativo está en docs/ARCHITECTURE.md §7. -->

Requisitos: Docker y GNU Make.

```sh
make up
```

Abre la web en <http://localhost:5173>; la API responde en <http://localhost:8000>. `make help` lista el resto de comandos, y `make check` ejecuta los checks de calidad. Para cambiar los puertos, copia `.env.example` como `.env`.

## Contribuir

- [`WORKFLOW.md`](WORKFLOW.md): el flujo de trabajo de principio a fin y el mapa de documentación.
- [`CONTRIBUTING.md`](CONTRIBUTING.md): ramas, commits, Issues, PRs y versiones.
- [`AGENTS.md`](AGENTS.md): instrucciones para agentes de IA.

## Licencia

Sin licencia definida.
