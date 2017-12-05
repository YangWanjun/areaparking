from django.apps import AppConfig


class EmployeeConfig(AppConfig):
    name = 'employee'
    icon = '<i class="material-icons">people</i>'
    verbose_name = '社員管理'
    order = 99
