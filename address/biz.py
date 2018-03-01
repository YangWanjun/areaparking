import googlemaps
import requests

from xml.etree import ElementTree

from master.models import Config
from utils.character import hira_to_kata


def geocode(address):
    coordinate = {'lng': 0, 'lat': 0, 'post_code': None}
    api_key = Config.get_google_map_key()
    if address and api_key:
        gmap = googlemaps.Client(key=api_key)
        geocode_result = gmap.geocode(address, language='ja')
        if len(geocode_result) > 0 and 'geometry' in geocode_result[0]:
            geometry = geocode_result[0].get('geometry')
            address_components = geocode_result[0].get('address_components')
            country = None
            for item in address_components:
                short_name = item.get('short_name')
                types = item.get('types')
                if short_name and short_name.upper() == "JP":
                    country = 'JP'
                if types and isinstance(types, list) and 'postal_code' in types:
                    coordinate['post_code'] = short_name
            if country:
                coordinate.update(geometry.get('location'))
    return coordinate


def get_furigana(name):
    json = {'hiragana': '', 'katakana': '', 'roman': ''}
    if name:
        app_id = Config.get_yahoo_app_id()
        url = Config.get_furigana_service()
        response = requests.post(url, data={'appid': app_id, 'sentence': name, 'output': 'json'})
        root = ElementTree.fromstring(response.content.decode('utf-8'))
        hiragana_list = []
        roman_list = []
        for word in root.iter('{urn:yahoo:jp:jlp:FuriganaService}Word'):
            furiganaNode = word.find('{urn:yahoo:jp:jlp:FuriganaService}Furigana')
            romanNode = word.find('{urn:yahoo:jp:jlp:FuriganaService}Roman')
            if furiganaNode is not None and furiganaNode.text:
                hiragana_list.append(furiganaNode.text)
            if romanNode is not None and romanNode.text:
                roman_list.append(romanNode.text)
        json['hiragana'] = "".join(hiragana_list)
        json['katakana'] = hira_to_kata(json['hiragana'])
        json['roman'] = " ".join(roman_list)
    return json
