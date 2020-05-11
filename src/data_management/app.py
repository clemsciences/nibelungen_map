
from flask import Flask, jsonify, request

from src.data_management.text_manager import NIBELUNGENLIED_TEXT, \
    get_text_size, find_places_mentioned_in_chapter
from src.data_management.place_manager import read_places_to_coordinates, \
    get_occurrences_lines

app = Flask(__name__)


@app.route("/places/")
def get_places():
    places_to_coordinates = read_places_to_coordinates()
    print(places_to_coordinates)
    return jsonify({"result": places_to_coordinates})


@app.route("/get-occurrences/", methods=["POST"])
def get_occurrences():
    data = request.get_json()
    if "placeType" in data:
        place_type = data["placeType"]
    else:
        return jsonify({"error": True})
    if "placeName" in data:
        place_name = data["placeName"]
    else:
        return jsonify({"error": True})
    occurrences, lines = get_occurrences_lines(NIBELUNGENLIED_TEXT,
                                               place_name, place_type)
    result = []
    for i in range(len(occurrences)):
        result.append({"occurrence": occurrences[i], "line": lines[i]})
    return jsonify({"result": result})


@app.route("/text/size/")
def get_text_size_json():
    return jsonify({"result": get_text_size()})


@app.route("/text/place-by-chapter/", methods=["POST"])
def get_places_in_chapter_json():
    data = request.get_json()
    print(data)
    result = []
    if "chapter" in data:
        chapter = data["chapter"]
        result = find_places_mentioned_in_chapter(int(chapter) - 1)
        print(result)
    return jsonify({"result": result})


if __name__ == "__main__":
    app.run()
