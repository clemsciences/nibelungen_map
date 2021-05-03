

from nibelungen_map_server import create_app
from nibelungen_map_server.routes import nibelungen_map


app = create_app(nibelungen_map, "")


if __name__ == "__main__":
    app.run(debug=True, port=5011)
