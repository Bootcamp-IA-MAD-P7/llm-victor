## 1. Targets de frontend

- [x] 1.1 Añadir `build-frontend` (`docker compose build frontend`) y `up-frontend` (`docker compose up -d --build --wait frontend`), y declararlos en `.PHONY`; verificar que ambos ejecutan lo esperado con `make build-frontend` y `make up-frontend`.
- [x] 1.2 Añadir `down-frontend`, `restart-frontend`, `ps-frontend`, `logs-frontend` y `shell-frontend` (`sh`), y declararlos en `.PHONY`; verificar cada target con el servicio en marcha.

## 2. Targets de api

- [x] 2.1 Añadir `build-api` (`docker compose build api`) y `up-api` (`docker compose up -d --build --wait api`), y declararlos en `.PHONY`; verificar que ambos ejecutan lo esperado.
- [x] 2.2 Añadir `down-api`, `restart-api`, `ps-api`, `logs-api` y `shell-api` (`sh`), y declararlos en `.PHONY`; verificar cada target con el servicio en marcha.

## 3. Targets de qdrant

- [x] 3.1 Añadir `pull-qdrant` (`docker compose pull qdrant`) y `up-qdrant` (`docker compose up -d --wait qdrant`, sin `--build`), y declararlos en `.PHONY`; verificar que `make pull-qdrant` descarga la imagen y que `make up-qdrant` arranca el servicio.
- [x] 3.2 Añadir `down-qdrant`, `restart-qdrant`, `ps-qdrant`, `logs-qdrant` y `shell-qdrant` (`sh`), y declararlos en `.PHONY`; verificar cada target con el servicio en marcha.

## 4. Borrado de volúmenes

- [x] 4.1 Añadir `clean-volumes` (`docker compose down --volumes`) y declararlo en `.PHONY`; verificar que borra el volumen de Qdrant y que `down` y `down-<servicio>` lo conservan.

## 5. Ayuda y documentación

- [x] 5.1 Actualizar `make help` con los targets por servicio y la advertencia de que `clean-volumes` borra datos; verificar la salida de `make help`.
- [x] 5.2 Actualizar [ARCHITECTURE §7](/docs/ARCHITECTURE.md#7-entorno-local-y-operación): mover los comandos por servicio y de borrado de volúmenes de «Objetivo» a Actual, con los nombres y ejemplos; verificar que no queda ninguna referencia contradictoria.

## 6. Verificación de extremo a extremo

- [x] 6.1 Con el conjunto arrancado, comprobar que operar un servicio (`restart-api`, `logs-frontend`, `shell-qdrant`, `down-frontend` y `up-frontend`) no altera el estado de los demás y que el volumen de Qdrant sobrevive a `down-qdrant`; verificar con `docker compose ps` y `docker volume ls`.
- [x] 6.2 Comprobar que los recipes no usan sintaxis exclusiva de Bash y que `make help` y los nuevos targets funcionan con GNU Make; verificar en el equipo local (Windows).
