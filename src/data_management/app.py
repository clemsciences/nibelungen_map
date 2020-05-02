
from flask import Flask, jsonify
from src.data_management.place_manager import read_places_to_coordinates

app = Flask(__name__)


@app.route("/places")
def get_places():
    places_to_coordinates = read_places_to_coordinates()
    print(places_to_coordinates)
    return jsonify(places_to_coordinates)


if __name__ == "__main__":
    app.run()
