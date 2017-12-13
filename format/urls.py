from django.conf.urls import url
from django.views import generic

from . import views


urlpatterns = [
    url('^$', generic.View.as_view(), name="index"),
    url('^subscription/(?P<report_id>\d+)/(?P<lot_id>\d+)/(?P<contractor_id>\d+)/$', views.SubscriptionView.as_view(),
        name="report_subscription"),
]
