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


def find_places_mentionned_in_chapter(chapter: int) -> List[str]:
    places = []
    for line in NIBELUNGENLIED_TEXT[chapter]:
        for half_line in line:
            for river in rivers:
                if river in half_line:
                    places.append(river)
            for city in cities:
                if city in half_line:
                    places.append(city)
            for region_country in regions_and_countries:
                if region_country in half_line:
                    places.append(region_country)
    return places
