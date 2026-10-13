# syntax=docker/dockerfile:1
FROM node:22-alpine AS base
WORKDIR /app

FROM base AS dev
COPY package.json package-lock.json ./
RUN npm ci
COPY . .
EXPOSE 5173
CMD ["npm", "run", "dev", "--", "--host", "0.0.0.0", "--port", "5173", "--strictPort"]

FROM base AS build
COPY package.json package-lock.json ./
RUN npm ci
COPY . .
# La URL pública de la API se fija al compilar; el build falla si falta (ARCHITECTURE §9).
ARG VITE_API_URL
RUN npm run build

FROM nginxinc/nginx-unprivileged:1.30.5-alpine AS prod
COPY nginx.conf /etc/nginx/conf.d/default.conf
COPY --from=build /app/dist /usr/share/nginx/html
EXPOSE 8080
