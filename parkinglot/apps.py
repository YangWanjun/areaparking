# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.apps import AppConfig


class ParkinglotConfig(AppConfig):
    name = 'parkinglot'
    icon = '<i class="material-icons">local_parking</i>'
    verbose_name = '物件管理'
    order = 20
