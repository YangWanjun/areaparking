# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf.urls import url, include


from . import views


urlpatterns = [
    url('^$', views.Index.as_view(), name="index"),
    url('^subscription/', include(views.SubscriptionVewSet().urls)),
    url('^subscription/(?P<task_id>\d+)/send_subscription_mail/$', views.SendSubscriptionMail.as_view(),
        name='send_subscription_mail'),
    url('^subscription/(?P<pk>\d+)/finish/$', views.SubscriptionFinish.as_view(), name='temp_contract_finish'),
    url('^subscription/(?P<pk>\d+)/destroy/$', views.SubscriptionDestroy.as_view(), name='subscription_destroy'),
    url('^subscription/(?P<task_id>\d+)/send_contract_mail/$', views.SendContractMail.as_view(),
        name='send_contract_mail'),

    url('^contract/', include(views.ContractVewSet().urls)),
    url('^contractor/', include(views.ContractorVewSet().urls)),
]
