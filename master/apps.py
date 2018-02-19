# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.apps import AppConfig

from utils.common import Setting
from utils import constants


class MasterConfig(AppConfig):
    name = 'master'
    icon = '<i class="material-icons">settings</i>'
    verbose_name = 'マスター設定'
    order = 99

    def ready(self):
        from .models import Config
        s = Setting()
        s.email_address = Config.get_value_by_name(constants.CONFIG_GROUP_EMAIL, constants.CONFIG_EMAIL_ADDRESS)
        s.email_smtp_host = Config.get_value_by_name(constants.CONFIG_GROUP_EMAIL, constants.CONFIG_EMAIL_SMTP_HOST)
        s.email_smtp_port = Config.get_value_by_name(constants.CONFIG_GROUP_EMAIL, constants.CONFIG_EMAIL_SMTP_PORT)
        s.email_password = Config.get_value_by_name(constants.CONFIG_GROUP_EMAIL, constants.CONFIG_EMAIL_PASSWORD)
        s.circle_radius = Config.get_circle_radius()
        s.domain_name = Config.get_domain_name()
        s.page_size = Config.get_page_size()
        s.decimal_type = Config.get_decimal_type()
        s.consumption_tax_rate = Config.get_consumption_tax_rate()
        s.car_length_adjust = Config.get_car_length_adjust()
        s.car_width_adjust = Config.get_car_width_adjust()
        s.car_height_adjust = Config.get_car_height_adjust()
        s.car_weight_adjust = Config.get_car_weight_adjust()
        s.url_timeout = Config.get_url_timeout()
        s.gcm_url = Config.get_gcm_url()
        s.firebase_serverkey = Config.get_firebase_serverkey()
        s.google_map_key = Config.get_google_map_key()
        s.parking_lot_key_alert_percent = Config.get_parking_lot_key_alert_percent()
