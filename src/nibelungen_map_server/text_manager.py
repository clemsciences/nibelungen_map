import re
from typing import Dict, List, Optional

from sigurd.nib_augsburg.nib_retrieval import MAIN_LINKS \
    as NIBELUNGEN_MAIN_LINKS
from sigurd.nib_augsburg.nib_reader import read_tei

from sigurd.nib_augsburg.nib_reader import read_rivers, \
    read_regions_and_countries, read_cities


__author__ = ["Clément Besnier <clem@clementbesnier.fr>", ]

NIBELUNGENLIED_TEXT = read_tei(NIBELUNGEN_MAIN_LINKS[0])

rivers = read_rivers()
cities = read_cities()
regions_and_countries = read_regions_and_countries()


def get_text_size():
    return len(NIBELUNGENLIED_TEXT)


def find_places_mentioned_in_chapter(chapter: int) -> List[str]:
    """
    >>> sorted(find_places_mentioned_in_chapter(1))
    ['Rhein', 'Xanten']

    :param chapter:
    :return:
    """
    places = []
    for line in NIBELUNGENLIED_TEXT[chapter]:
        for half_line in line:
            for river in rivers:
                places.extend([river for river_token in rivers[river]
                               if river_token in half_line])
            for city in cities:
                places.extend([city for city_token in cities[city]
                               if city_token in half_line])
            for region_country in regions_and_countries:

                places.extend([region_country
                               for region_country_token in regions_and_countries[region_country]
                               if region_country_token in half_line])
    return list(set(places))


def build_place_token_index() -> Dict[str, Dict[str, str]]:
    """
    >>> build_place_token_index()["Roten"]
    {'name': 'Rhone', 'placeType': 'river'}

    :return: mapping from a token of the text to the place it refers to
    """
    index = {}
    for place_type, places in [("river", rivers), ("city", cities),
                               ("region_country", regions_and_countries)]:
        for place_name, tokens in places.items():
            for token in tokens:
                index[token.strip()] = {"name": place_name,
                                        "placeType": place_type}
    return index


PLACE_TOKEN_INDEX = build_place_token_index()


def normalize_token(token: str) -> str:
    """
    Remove editorial marks (brackets, apostrophes...) so that a token can be
    compared to the annotated place tokens.

    >>> normalize_token("[Wormez]")
    'Wormez'

    :param token:
    :return:
    """
    return re.sub(r"[^\w]", "", token)


def find_place_of_token(token: str) -> Optional[Dict[str, str]]:
    """
    >>> find_place_of_token("Rine")
    {'name': 'Rhein', 'placeType': 'river'}
    >>> find_place_of_token("chint") is None
    True

    :param token:
    :return:
    """
    return PLACE_TOKEN_INDEX.get(normalize_token(token))


def annotate_chapter(chapter: int, located_place_names: List[str]) -> List[Dict]:
    """
    Split a chapter into tokens and annotate the ones which refer to a place.

    >>> lines = annotate_chapter(0, ["Rhein"])
    >>> lines[20]["line"]
    21
    >>> [t for half_line in lines[20]["halfLines"] for t in half_line if t["place"]]
    [{'token': 'Wormze', 'place': {'name': 'Worms', 'placeType': 'city', 'located': False}}, {'token': 'Rine', 'place': {'name': 'Rhein', 'placeType': 'river', 'located': True}}]

    :param chapter: index of the chapter (starts at 0)
    :param located_place_names: names of places which have coordinates
    :return: lines of the chapter
    """
    lines = []
    for i, line in enumerate(NIBELUNGENLIED_TEXT[chapter]):
        half_lines = []
        for half_line in line:
            tokens = []
            for token in (half_line or "").split(" "):
                place = find_place_of_token(token)
                if place:
                    place = dict(place, located=place["name"] in located_place_names)
                tokens.append({"token": token, "place": place})
            half_lines.append(tokens)
        lines.append({"line": i + 1, "halfLines": half_lines})
    return lines
