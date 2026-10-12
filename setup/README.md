# Adopción de la plantilla

Pasos que se hacen una sola vez al crear un proyecto a partir de esta plantilla. Al terminar, borra la carpeta `setup/`.

1. [ ] Crea el repositorio a partir de la plantilla. Su contenido queda en `main`.
2. [ ] Instala las herramientas y ejecuta `openspec init` con el perfil expandido ([WORKFLOW §3](../WORKFLOW.md#3-herramientas)).
3. [ ] Rellena los textos entre corchetes del [`README.md`](../README.md), incluido `[owner]/[repo]`, y borra su comentario inicial. Añade una licencia si procede.
4. [ ] Borra la carpeta `setup/` y haz el commit inicial en `main`: `chore: adopt project template`.
5. [ ] Crea la rama `dev` desde `main` y publica las dos.
6. [ ] En GitHub:
   - cambia la rama por defecto a `dev`, para que `Closes #N` cierre las Issues al mergear en ella;
   - en los ajustes de merge, permite *Rebase and merge* y *Create a merge commit*, y desactiva *Squash and merge*.
7. [ ] Pide a la IA que empiece la fase de definición ([WORKFLOW §4](../WORKFLOW.md#4-fase-1--definición)).
