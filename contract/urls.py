# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf.urls import url, include


from . import views


urlpatterns = [
    url('^$', views.Index.as_view(), name="index"),
    url('^temp_contract/', include(views.TempContractVewSet().urls)),
    url('^contract/', include(views.ContractVewSet().urls)),
    url('^contractor/', include(views.ContractorVewSet().urls)),
    url('^temp_contract/(?P<task_id>\d+)/send_subscription_mail/$', views.SendSubscriptionMail.as_view(),
        name='send_subscription_mail'),
    url('^temp_contract/(?P<pk>\d+)/finish/$', views.TempContractFinish.as_view(), name='temp_contract_finish'),
    url('^temp_contract/(?P<pk>\d+)/destroy/$', views.TempContractDestroy.as_view(), name='temp_contract_destroy'),
]
