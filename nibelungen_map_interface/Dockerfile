# Build stage: compiles the Vue app with Vite
FROM node:22-alpine AS build
WORKDIR /app

COPY package.json yarn.lock ./
RUN yarn install --frozen-lockfile

COPY . .

# The API URL is baked into the bundle at build time.
# Defaults to .env.production; override with --build-arg VITE_SITE_API_URL=...
ARG VITE_SITE_API_URL
RUN if [ -z "$VITE_SITE_API_URL" ]; then unset VITE_SITE_API_URL; fi && yarn build

# Serve stage: static files only
FROM nginx:1.29-alpine
COPY --from=build /app/nibelungen-map-dist /usr/share/nginx/html
EXPOSE 80
