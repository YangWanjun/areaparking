# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf.urls import url, include

from . import views


urlpatterns = [
    url('^$', views.Index.as_view(), name="index"),
    url('^whiteboard/', include(views.WhiteBoardViewSet().urls)),
    url('^whiteboard-position-(?P<pk>\d+)\.html', views.WhiteBoardPositionDetailView.as_view(),
        name='whiteboard_position_detail'),
    url('^waiting/', include(views.WaitingViewSet().urls)),
    url('^map.html$', views.WhiteBoardMapView.as_view(), name='whiteboard_map'),
    url('^inquiry/', include(views.InquiryViewSet().urls)),

    url('^update_subscription$', views.UpdateSubscription.as_view(), name='update_subscription'),
    url('^notification_data/\.json$', views.GetNotificationData.as_view(), name='notification_data'),
]
