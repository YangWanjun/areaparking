from . import models
from utils import common, constants


def get_lacking_keys():
    """

    :return:
    """
    parking_lot_lacking_keys = list()
    # 鍵の持つ駐車場
    queryset = models.ParkingLot.objects.public_filter(
        parkingposition__isnull=False,
        parkingposition__parkingpositionkey__isnull=False
    ).distinct()
    for parking_lot in queryset:
        lacking_keys = parking_lot.get_lacking_keys()
        for category, count in lacking_keys:
            name = common.get_choice_name_by_key(constants.CHOICE_KEY_CATEGORY, category)
            parking_lot_lacking_keys.append((parking_lot, category, name, count))
    return parking_lot_lacking_keys
