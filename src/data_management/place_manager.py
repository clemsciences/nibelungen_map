"""

"""
import codecs
import json
import os
import time
from typing import List, Dict
from sigurd.nib_augsburg.nib_reader import read_rivers, \
    read_regions_and_countries, read_cities
from src.data_management import PACKDIR

import requests

__author__ = ["Clément Besnier <clem@clementbesnier.fr>", ]


def make_dict_place(place_name: str, place_type: str) -> Dict[str, str]:
    return {"name": place_name, "placeType": place_type}


def get_places() -> List[Dict[str, str]]:
    """
    >>> get_places()[0]
    'Alzey'

    :return:
    """
    place_names = [make_dict_place(key, "river") for key in read_rivers()]
    place_names.extend([make_dict_place(key, "region_country")
                        for key in read_regions_and_countries()])
    place_names.extend([make_dict_place(key, "city") for key in read_cities()])
    return place_names


def request_place(place_name: str) -> Dict[str, Dict[str, str]]:
    """
    >>> request_place("Xanten")
    {'Xanten': {'lat': '51.661519', 'lon': '6.4543203'}}

    :param place_name: name of the place
    :return:
    """
    name_to_coordinates = None
    res = requests.get("https://nominatim.openstreetmap.org/search",
                       {"q": place_name, "format": "json",
                        "accept-language": "de"})
    decoded_res = json.loads(res.content, encoding=res.encoding)
    if decoded_res and len(decoded_res) > 0:
        name_to_coordinates = {"lat": decoded_res[0]["lat"],
                               "lon": decoded_res[0]["lon"],
                               "name": place_name}
    return name_to_coordinates


def get_places_to_coordinates(places: List[Dict[str, str]]):
    """
    >>>

    :param places:
    :return:
    """
    places_to_coordinates = []
    for place in places:
        located_place = request_place(place["name"])
        if located_place:
            located_place["placeType"] = place["placeType"]
            places_to_coordinates.append(located_place)
        time.sleep(1)
    return places_to_coordinates


def retrieve_and_save_places_to_coordinates():
    places = get_places()
    places_to_coordinates = get_places_to_coordinates(places)
    with codecs.open(os.path.join(PACKDIR, "data", "retrieved", "nibelungenlied_places.json"),
                     "wb", encoding="utf-8") as f:
        json.dump(places_to_coordinates, f)


def read_places_to_coordinates():
    """

    :return:
    """
    path_and_filename = os.path.join(PACKDIR, "data", "retrieved", "nibelungenlied_places.json")
    print(path_and_filename)
    if os.path.exists(path_and_filename):
        print("ok")
        with codecs.open(path_and_filename,
                         "rb", encoding="utf-8") as f:
            return json.load(f)
    return None


if __name__ == "__main__":
    retrieve_and_save_places_to_coordinates()
