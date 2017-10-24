# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf.urls import url, include
from django.views import generic

from . import views


urlpatterns = [
    url('^$', generic.TemplateView.as_view(template_name="whiteboard/index.html"), name="index"),
    # url('^whiteboard/', include(views.ParkingLotViewSet().urls)),
]
