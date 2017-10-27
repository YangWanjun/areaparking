# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.apps import AppConfig

from material.frontend.apps import ModuleMixin


class TurnoverConfig(ModuleMixin, AppConfig):
    name = 'turnover'
    icon = '<i class="material-icons">pie_chart</i>'
    verbose_name = '賃貸状況一覧'
    order = 40
