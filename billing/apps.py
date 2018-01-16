from django.apps import AppConfig

from material.frontend.apps import ModuleMixin


class BillingConfig(ModuleMixin, AppConfig):
    name = 'billing'
    icon = '<i class="material-icons">attach_money</i>'
    verbose_name = '請求管理'
    order = 40
