import googlemaps

from master.models import Config


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
