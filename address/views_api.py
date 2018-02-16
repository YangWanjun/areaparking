import googlemaps

from rest_framework import viewsets
from rest_framework.response import Response

from master.models import Config


class GeocodeViewSet(viewsets.ViewSet):

    def list(self, request, format=None):
        address = request.GET.get('address', None)
        coordinate = {'lng': 0, 'lat': 0}
        api_key = Config.get_google_map_key()
        if address and api_key:
            gmap = googlemaps.Client(key=api_key)
            geocode_result = gmap.geocode(address)
            if len(geocode_result) > 0 and 'geometry' in geocode_result[0]:
                geometry = geocode_result[0].get('geometry')
                address_components = geocode_result[0].get('address_components')
                countries = [item for item in address_components if item.get('short_name').upper() == "JP"]
                if len(countries) > 0:
                    coordinate = geometry.get('location')
        return Response(coordinate)
