# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf.urls import url

from rest_framework import routers

from . import views, views_api


router = routers.DefaultRouter()
router.register(r'whiteboard', views_api.WhiteBoardViewSet)

urlpatterns = [
    url('^$', views.Index.as_view(), name="index"),
    url('^whiteboard/$', views.WhiteBoardListView.as_view(), name='whiteboard_list'),
    url('^whiteboard/(?P<id>\d+)/$', views.WhiteBoardDetailView.as_view(), name='whiteboard_detail'),
    # url('^parking-lot-(?P<id>\d+)\.html', views.ParkingLotDetail.as_view(), name='parking-lot-detail'),
    # url('^parking-position-(?P<id>\d+)\.html', views.ParkingPositionDetail.as_view(), name='parking-position-detail'),
    # url('^whiteboard/', include(views.WhiteBoardViewSet().urls)),
    # url('^waiting/', include(views.WaitingListViewSet().urls)),
    url('^map.html$', views.WhiteBoardMapView.as_view(), name='whiteboard_map')
]
