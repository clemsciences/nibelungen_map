from typing import List

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
