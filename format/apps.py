from django.apps import AppConfig


class FormatConfig(AppConfig):
    name = 'format'
    icon = '<i class="material-icons">vibration</i>'
    verbose_name = '出力書式'
    order = 99
