from django.contrib.gis.geos import Point

from rest_framework_gis.serializers import GeoFeatureModelSerializer, GeometrySerializerMethodField

from . import models


class WhiteBoardSerializer(GeoFeatureModelSerializer):
    point = GeometrySerializerMethodField()

    class Meta:
        model = models.WhiteBoard
        fields = ('parking_code', 'parking_lot_name', 'address', 'lng', 'lat', 'point', 'position_count', 'free_end_date')
        geo_field = 'point'

    def get_point(self, obj):
        return Point(obj.lng, obj.lat, srid=4326)
