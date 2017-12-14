from django.conf.urls import url
from django.views import generic

from . import views


urlpatterns = [
    url('^$', generic.View.as_view(), name="index"),
    url('^user_subscription/(?P<task_id>\d+)\.html$', views.UserOperationView.as_view(), name="user_subscription"),
    url('^subscription_confirm/(?P<report_id>\d+)/(?P<lot_id>\d+)/(?P<contractor_id>\d+)/$',
        views.SubscriptionConfirmView.as_view(), name="report_subscription_confirm"),
]
