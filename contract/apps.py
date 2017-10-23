# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.apps import AppConfig

from material.frontend.apps import ModuleMixin


class ContractConfig(AppConfig):
    name = 'contract'
    icon = '<i class="material-icons">done_all</i>'
    verbose_name = '契約管理'
    order = 31
