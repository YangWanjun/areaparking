# -*- coding: utf-8 -*-
"""areaparking URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from __future__ import unicode_literals
from django.conf import settings
from django.conf.urls import url, include
from django.contrib.auth import views as auth_views
from django.views import generic
from django.views.static import serve

from material import frontend
from material.frontend.apps import ModuleMixin
from material.frontend.registry import modules

from parkinglot import urls as parkinglot_urls
from contract.urls import router as contract_router


class Home(ModuleMixin):
    """
    Home page module
    """
    order = 1
    label = 'Home'
    verbose_name = 'ホーム'
    icon = '<i class="material-icons">account_balance</i>'

    @property
    def urls(self):
        index_view = generic.TemplateView.as_view(template_name='index.html')

        return frontend.ModuleURLResolver(
            '^', [url('^$', index_view, name="index")],
            module=self, app_name='areaparking', namespace='home')

    def index_url(self):
        return '/'

    def installed(self):
        return True


modules.register(Home())

from material.frontend import urls as frontend_urls

urlpatterns = [
    url(r'', include(frontend_urls)),
    url(r'^parkinglot/', include(parkinglot_urls)),
    # url(r'^admin/login/$', auth_views.logout, name="logout"),
    url(r'^admin/login/$', auth_views.login, name="login"),

    url(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),

    url(r'^api/', include(contract_router.urls)),
]
