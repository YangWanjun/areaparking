import os
from django.contrib.gis.utils import LayerMapping
from django.db import connection

from .models import AzaTest
from utils import common


aza_mapping = {
    'KEY_CODE': 'KEY_CODE',
    'PREF': 'PREF',
    'CITY': 'CITY',
    'S_AREA': 'S_AREA',
    'PREF_NAME': 'PREF_NAME',
    'CITY_NAME': 'CITY_NAME',
    'S_NAME': 'S_NAME',
    'KIGO_E': 'KIGO_E',
    'HCODE': 'HCODE',
    'AREA': 'AREA',
    'PERIMETER': 'PERIMETER',
    'H27KAxx': 'H27KAxx_',
    'H27KAxx_ID': 'H27KAxx_ID',
    'KEN': 'KEN',
    'KEN_NAME': 'KEN_NAME',
    'SITYO_NAME': 'SITYO_NAME',
    'GST_NAME': 'GST_NAME',
    'CSS_NAME': 'CSS_NAME',
    'KIHON1': 'KIHON1',
    'DUMMY1': 'DUMMY1',
    'KIHON2': 'KIHON2',
    'KEYCODE1': 'KEYCODE1',
    'KEYCODE2': 'KEYCODE2',
    'AREA_MAX_F': 'AREA_MAX_F',
    'KIGO_D': 'KIGO_D',
    'N_KEN': 'N_KEN',
    'N_CITY': 'N_CITY',
    'KIGO_I': 'KIGO_I',
    'MOJI': 'MOJI',
    'KBSUM': 'KBSUM',
    'JINKO': 'JINKO',
    'SETAI': 'SETAI',
    'X_CODE': 'X_CODE',
    'Y_CODE': 'Y_CODE',
    'KCODE1': 'KCODE1',
    'mpoly': 'MULTIPOLYGON',
}

root_path = os.path.join(common.get_data_path(), 'ADDRESS', 'aza_polygon')


def run(verbose=True):
    for name in os.listdir(root_path):
        if name[-4:] == ".shp":
            shp_path = os.path.join(root_path, name)
            lm = LayerMapping(
                AzaTest, shp_path, aza_mapping,
                transform=False, encoding='UTF-8',
            )
            lm.save(strict=True, verbose=verbose)
    with connection.cursor() as cursor:
        cursor.execute("truncate gis_aza")
        cursor.execute("insert into areaparking.gis_aza (code, name, full_name, point, mpoly, people_count, home_count, city_id, pref_id, created_date, updated_date, is_deleted, deleted_date) "
                       "select key_code as code, s_name as name, concat(PREF_NAME, CITY_NAME, S_NAME) as full_name, POINT(X_CODE, Y_CODE), mpoly, jinko, setai, concat(PREF, CITY) as city_id, PREF as pref_id"
                       "     , created_date, updated_date, is_deleted, deleted_date"
                       "  from areaparking.gis_aza_polygon"
                       " where exists (select 1 from gis_city where concat(gis_aza_polygon.PREF, gis_aza_polygon.CITY) = gis_city.code)")
        cursor.execute("truncate gis_aza_test")
