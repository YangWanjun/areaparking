# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.apps import AppConfig


class MasterConfig(AppConfig):
    name = 'master'
    icon = '<i class="material-icons">settings</i>'
    verbose_name = 'マスター設定'
    order = 99
