# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.apps import AppConfig

from material.frontend.apps import ModuleMixin


class WhiteboardConfig(ModuleMixin, AppConfig):
    name = 'whiteboard'
    icon = '<i class="material-icons">airplay</i>'
    verbose_name = 'ホワイトボード'
    order = 20
