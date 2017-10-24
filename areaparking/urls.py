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
from django.conf import settings
from django.conf.urls import url, include
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.shortcuts import render
from django.views import generic

from material import frontend
from material.frontend import urls as frontend_urls
from material.frontend.apps import ModuleMixin
from material.frontend.registry import modules

from parkinglot import urls as parkinglot_urls


class Demo(ModuleMixin):
    """
    Home page module
    """
    order = 1
    label = 'Introduction'
    icon = '<i class="material-icons">account_balance</i>'

    @property
    def urls(self):
        index_view = generic.TemplateView.as_view(template_name='demo/index.html')

        return frontend.ModuleURLResolver(
            '^', [url('^$', index_view, name="index")],
            module=self, app_name='oa', namespace='demo')

    def index_url(self):
        return '/'

    def installed(self):
        return True


modules.register(Demo())


urlpatterns = [
    # url(r'^$', generic.TemplateView.as_view(template_name='index.html')),

    url(r'', include(frontend_urls)),
    url(r'^parkinglot/', include(parkinglot_urls)),
    # url(r'^admin/login/$', auth_views.logout, name="logout"),
    url(r'^admin/login/$', auth_views.login, name="login"),
] # + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
