# nibelungen_map_interface

## Project setup
```
yarn install
```

Requires Node.js 20.19+ or 22.13+.

### Compiles and hot-reloads for development
```
yarn dev
```

### Compiles and minifies for production
```
yarn build
```
Output goes to `nibelungen-map-dist/`.

### Lints files
```
yarn lint
```

### Docker
```
docker build -t nibelungen-map-interface .
docker run -p 8080:80 nibelungen-map-interface
```
The API URL is baked in at build time (default: `.env.production`). Override it with `--build-arg VITE_SITE_API_URL=...`.

### Customize configuration
See [Vite Configuration Reference](https://vite.dev/config/).
