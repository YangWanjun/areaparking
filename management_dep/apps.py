from django.apps import AppConfig

from material.frontend.apps import ModuleMixin


class ManagementDepConfig(ModuleMixin, AppConfig):
    name = 'management_dep'
    icon = '<i class="material-icons">business</i>'
    verbose_name = '管理部関連'
    order = 50
