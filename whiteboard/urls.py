# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf.urls import url, include

from . import views


urlpatterns = [
    url('^$', views.Index.as_view(), name="index"),
    # url('^parking-lot-(?P<id>\d+)\.html', views.ParkingLotDetail.as_view(), name='parking-lot-detail'),
    # url('^parking-position-(?P<id>\d+)\.html', views.ParkingPositionDetail.as_view(), name='parking-position-detail'),
    url('^whiteboard/', include(views.WhiteBoardViewSet().urls)),
    # url('^waiting/', include(views.WaitingListViewSet().urls)),
    url('^map.html$', views.WhiteBoardMapView.as_view(), name='whiteboard_map')
]
