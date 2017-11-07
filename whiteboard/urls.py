# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf.urls import url, include
from django.views import generic

from . import views


urlpatterns = [
    url('^$', views.ParkingPositionListView.as_view(), name="index"),
    url('^parking-lot-(?P<id>\d+)\.html', views.ParkingLotDetail.as_view(), name='parking-lot-detail'),
    url('^parking-position-(?P<id>\d+)\.html', views.ParkingPositionDetail.as_view(), name='parking-position-detail'),
    url('^waiting-list\.html', views.WaitingListView.as_view(), name='waiting-list'),
    url('^whiteboard/', include(views.WhiteBoardViewSet().urls)),
]
