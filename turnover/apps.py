from django.apps import AppConfig

from material.frontend.apps import ModuleMixin


class TurnoverConfig(ModuleMixin, AppConfig):
    name = 'turnover'
    icon = '<i class="material-icons">pie_chart</i>'
    verbose_name = '経営データ'
    order = 60

    def index_url(self):
        return None
