# ADR-0001: Docker-first y servicios desplegables por separado

- **Estado:** Aceptado
- **Fecha:** 2026-10-05
- **Decisores:** Glezino
- **Relacionado:** RNF-05, [ARCHITECTURE §7 y §9](../ARCHITECTURE.md#7-entorno-local-y-operación)

## Contexto

AI Content Studio necesita desde el inicio varios servicios: web, API de generación y Qdrant. El desarrollo debe funcionar en local, levantar el conjunto con un único comando y permitir arrancar y operar cada servicio por separado. No hay servidor propio: aunque esta fase no despliega en producción, los servicios de aplicación deben poder desplegarse por separado en plataformas gestionadas cuando el roadmap lo priorice.

## Decisión

- Contenerizar la web y la API desde el inicio y usar la imagen oficial de Qdrant.
- Usar Docker Compose como entorno local, para el sistema completo o para servicios sueltos.
- Dar a cada servicio desplegable su propio Dockerfile y su configuración externa.
- Añadir un Makefile con comandos globales y por servicio para las operaciones habituales.
- Mantener configurables los proveedores y destinos externos, sin desplegar ni contratar nada como parte de esta decisión.

## Alternativas consideradas

- **Ejecutar las aplicaciones directamente en la máquina, sin contenedores:** no reduce las diferencias entre entornos ni facilita probar Qdrant junto con la aplicación.

## Consecuencias

- La configuración local y las imágenes sirven de base para el despliegue futuro; Compose es solo para desarrollo y cada plataforma configurará sus servicios por separado.
- Los servicios se comunican mediante direcciones y secretos configurables, sin asumir nombres ni puertos fijos de una plataforma: la web recibe la URL de la API por entorno y la API parametriza CORS.
- Docker añade configuración y consumo de recursos en desarrollo.
