import os
from django.contrib.gis.utils import LayerMapping

from .models import AzaPolygon
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
                AzaPolygon, shp_path, aza_mapping,
                transform=False, encoding='UTF-8',
            )
            lm.save(strict=True, verbose=verbose)
