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
    url('^contract/', include(views.ContractVewSet().urls)),
    url('^contractor/', include(views.ContractorVewSet().urls)),
    url('^temp_contract/(?P<id>\d+)/$', views.TempContractDetailView.as_view(), name='tempcontract_detail'),
    url('^temp_contract/(?P<task_id>\d+)/send_subscription_mail/$', views.SendSubscriptionMail.as_view(),
        name='send_subscription_mail'),
]
