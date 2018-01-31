# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf.urls import url, include


from . import views


urlpatterns = [
    url('^$', views.Index.as_view(), name="index"),
    url('^subscription/', include(views.SubscriptionVewSet().urls)),
    url('^subscription/(?P<task_id>\d+)/send_subscription_mail/$', views.SendSubscriptionMail.as_view(),
        name='send_subscription_mail'),
    url('^subscription/(?P<pk>\d+)/finish/$', views.SubscriptionFinish.as_view(), name='subscription_finish'),
    url('^subscription/(?P<pk>\d+)/destroy/$', views.SubscriptionDestroy.as_view(), name='subscription_destroy'),
    url('^subscription/(?P<task_id>\d+)/send_contract_mail/$', views.SendContractMail.as_view(),
        name='send_contract_mail'),
    url('^task/(?P<task_id>\d+)/send_task_mail/$', views.SendTaskMail.as_view(),
        name='send_task_mail'),

    url('^contracted-parking-lot/', include(views.ContractedParkingLotViewSet().urls)),
    url('^contract/', include(views.ContractVewSet().urls)),
    url('^contractor/', include(views.ContractorVewSet().urls)),
    url('^process/', include(views.ProcessViewSet().urls)),
    # url('^price-raise/', include(views.VPriceRaiseViewSet().urls)),

    url('^price-raise-list/$', views.PriceRaiseListView.as_view(), name='priceraise_list'),
    url('^price-raising-list/$', views.PriceRaisingListView.as_view(), name='priceraising_list'),

    url('^trouble/$', views.TroubleListView.as_view(), name='trouble_list'),
    url('^trouble/(?P<pk>\d+)/detail/$', views.TroubleDetailView.as_view(), name='trouble_detail'),
    url('^trouble/add/$', views.TroubleAddView.as_view(), name='trouble_add'),
    url('^defect/$', views.DefectListView.as_view(), name='defect_list'),
    url('^defect/(?P<pk>\d+)/detail/$', views.DefectDetailView.as_view(), name='defect_detail'),
    url('^defect/add/$', views.DefectAddView.as_view(), name='defect_add'),
    url('^voluntary-insurance-list/$', views.VoluntaryInsuranceListView.as_view(), name='voluntary_insurance_list'),
]
