# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf.urls import url
from django.views import generic


urlpatterns = [
    url('^$', generic.TemplateView.as_view(template_name="parkinglot/index.html"), name="index"),
]
