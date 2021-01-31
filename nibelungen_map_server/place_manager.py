"""

"""
import codecs
import enum
import json
import os
import time
from typing import List, Dict
from sigurd.nib_augsburg.nib_reader import find_occurrences_in_text

from nibelungen_map_server import PACKDIR

from nibelungen_map_server.text_manager import NIBELUNGENLIED_TEXT, \
    regions_and_countries, cities, rivers

import requests

__author__ = ["Clément Besnier <clem@clementbesnier.fr>", ]


class Place(enum.Enum):
    river = enum.auto()
    region_country = enum.auto()
    city = enum.auto()


def make_dict_place(place_name: str, place_type: str, tokens: List[str]) \
        -> Dict[str, str]:
    return {"name": place_name, "placeType": place_type, "tokens": tokens}


def extract_indices(indices: str, text, limit: int):
    """
    >>> extract_indices("1-1-1-1", NIBELUNGENLIED_TEXT, 3)
    'UNS IST> In alten'

    :param indices:
    :param text:
    :param limit:
    :return:
    """
    assert 1 <= limit <= 4
    chapter, line, half_line, token = indices.split("-")
    if limit == 1:
        return text[int(chapter)-1]
    elif limit == 2:
        return text[int(chapter)-1][int(line)-1]
    elif limit == 3:
        return text[int(chapter)-1][int(line)-1][int(half_line)-1]
    elif limit == 4:
        return text[int(chapter)-1][int(line)-1][int(half_line)-1][int(token)-1]


def get_place_tokens(place_name: str, place_type: str) -> List[str]:
    """
    >>> get_place_tokens("Rhone", Place.river.name)
    ['Roten']

    :param place_name:
    :param place_type:
    :return:
    """
    place_tokens = []
    if place_type == Place.river.name:
        if place_name in rivers:
            place_tokens = rivers[place_name]
    elif place_type == Place.region_country.name:
        if place_name in regions_and_countries:
            place_tokens = regions_and_countries[place_name]
    elif place_type == Place.city.name:
        if place_name in cities:
            place_tokens = cities[place_name]
    return place_tokens


def get_occurrences_lines(text, place_name, place_type):
    """

    >>> occurrences, lines = get_occurrences_lines(NIBELUNGENLIED_TEXT, "Rhone", Place.river.name)
    >>> occurrences
    ['31-410-1-2']

    >>> lines
    [['vonme Roten zv dem Rine', 'vf bi Elbe vnz an daz mer']]

    :param text:
    :param place_name:
    :param place_type:
    :return:
    """
    occurrences = find_occurrences_in_text(text, get_place_tokens(place_name, place_type))
    lines = [extract_indices(index, text, 2) for index in occurrences]
    return occurrences, lines


def get_places() -> List[Dict[str, str]]:
    """
    >>> get_places()[4]
    {'name': 'Rhone', 'placeType': 'river', 'tokens': ['Roten']}

    :return:
    """
    place_names = [make_dict_place(key, "river", rivers[key]) for key in rivers]
    place_names.extend([make_dict_place(key, "region_country",
                                        regions_and_countries[key])
                        for key in regions_and_countries])
    place_names.extend([make_dict_place(key, "city", cities[key])
                        for key in cities])
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
    with codecs.open(os.path.join(PACKDIR, "data", "retrieved",
                                  "nibelungenlied_places.json"),
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
