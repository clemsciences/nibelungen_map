"""

"""
import codecs
import json
import os
import time
from typing import List, Dict
from sigurd.nib_augsburg.nib_reader import read_places
from src.data_management import PACKDIR

import requests

__author__ = ["Clément Besnier <clem@clementbesnier.fr>", ]


def get_place_names():
    """
    >>> get_place_names()[0]
    'Alzey'

    :return:
    """
    place_names = [key for key in read_places()]
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
                       {"q": place_name, "format": "json", "accept-language": "de"})
    decoded_res = json.loads(res.content, encoding=res.encoding)
    if decoded_res and len(decoded_res) > 0:
        name_to_coordinates = {"lat": decoded_res[0]["lat"],
                               "lon": decoded_res[0]["lon"],
                               "name": place_name}
    return name_to_coordinates


def get_places_to_coordinates(places: List[str]):
    """
    >>>

    :param places:
    :return:
    """
    places_to_coordinates = []
    for place_name in places:
        print(place_name)
        places_to_coordinates.append(request_place(place_name))
        time.sleep(1)
    return places_to_coordinates


def retrieve_and_save_places_to_coordinates():
    place_names = get_place_names()
    places_to_coordinates = get_places_to_coordinates(place_names)
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
