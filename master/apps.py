# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.apps import AppConfig

from material.frontend.apps import ModuleMixin


class MasterConfig(ModuleMixin, AppConfig):
    name = 'master'
    icon = '<i class="material-icons">settings</i>'
    verbose_name = 'マスター設定'
    order = 99
