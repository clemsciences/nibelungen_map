# Nibelungen map

Map with places mentioned in Nibelungenlied.

## How to use it

### Server

With [uv](https://docs.astral.sh/uv/):

```bash
uv sync
uv run nibelungen-map-server   # http://127.0.0.1:5011
```

Without uv (`sigurd`'s unused dependencies are skipped, they don't build on Python 3.14):

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install --no-deps -r requirements.txt
nibelungen-map-server
```

### Server with Docker

```bash
docker build -t nibelungen-map-server .
docker run -p 5011:5011 nibelungen-map-server
```
