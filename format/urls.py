from django.conf.urls import url
from django.views import generic

from . import views


urlpatterns = [
    url('^$', generic.View.as_view(), name="index"),
    url('^user_subscription/(?P<signature>[^/]+)\.html$', views.UserOperationView.as_view(), name="user_subscription"),
    url('^subscription_confirm/(?P<task_id>\d+)/(?P<report_id>\d+)/$',
        views.SubscriptionConfirmView.as_view(), name="report_subscription_confirm"),
    url('^subscription/(?P<task_id>\d+)/(?P<report_id>\d+)/$',
        views.SubscriptionView.as_view(), name="report_subscription"),
    url('^url_timeout\.html$', views.UrlTimeoutView.as_view(), name='url_timeout'),

    # Download PDF
    url('^download/pdf/subscription_confirm/(?P<task_id>\d+)/(?P<report_id>\d+)/$',
        views.GenerateSubscriptionConfirmPdfView.as_view(), name='download_report_subscription_confirm'),
    url('^download/pdf/subscription/(?P<task_id>\d+)/(?P<report_id>\d+)/$',
        views.GenerateSubscriptionPdfView.as_view(), name='download_report_subscription'),

    # url(r'^user_subscription/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
    #     views.UserOperationView.as_view(), name='activate_account'),
]
