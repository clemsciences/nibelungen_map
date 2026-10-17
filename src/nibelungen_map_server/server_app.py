"""

"""

from flask_cors import CORS

from nibelungen_map_server import create_app
from nibelungen_map_server.routes import nibelungen_map


app = create_app(nibelungen_map, "")
cors = CORS()
cors.init_app(app)
