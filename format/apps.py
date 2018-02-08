from django.apps import AppConfig

from material.frontend.apps import ModuleMixin


class FormatConfig(ModuleMixin, AppConfig):
    name = 'format'
    icon = '<i class="material-icons">vibration</i>'
    verbose_name = '出力書式'
    order = 99

    def is_hide(self):
        return True
