# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf.urls import url, include

from rest_framework import routers

from . import views, views_api


router = routers.DefaultRouter()
router.register(r'temp-contractor', views_api.TempContractorViewSet)
router.register(r'temp-contract', views_api.TempContractViewSet)


urlpatterns = [
    url('^$', views.TempContractListView.as_view(), name="index"),
    url('^temp_contract/create/$', views.CreateTempContractView.as_view(), name='create_temp_contract'),
    url('^temp_contract/(?P<id>\d+)/$', views.TempContractDetailView.as_view(), name='tempcontract_detail'),
]
