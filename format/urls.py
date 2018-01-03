from django.conf.urls import url
from django.views import generic

from . import views


urlpatterns = [
    url('^$', generic.View.as_view(), name="index"),
    url('^user_subscription_step1/(?P<pk>\d+)/(?P<signature>[^/]+)\.html$', views.UserSubscriptionStep1View.as_view(),
        name="user_subscription_step1"),
    url('^user_subscription_step2/(?P<pk>\d+)/(?P<signature>[^/]+)\.html$', views.UserSubscriptionStep2View.as_view(),
        name="user_subscription_step2"),
    url('^user_subscription_step3/(?P<pk>\d+)/(?P<signature>[^/]+)\.html$', views.UserSubscriptionStep3View.as_view(),
        name="user_subscription_step3"),
    url('^user_subscription_step4/(?P<pk>\d+)/(?P<signature>[^/]+)\.html$', views.UserSubscriptionStep4View.as_view(),
        name="user_subscription_step4"),
    url('^user_subscription_step5/(?P<pk>\d+)/(?P<signature>[^/]+)\.html$', views.UserSubscriptionStep5View.as_view(),
        name="user_subscription_step5"),
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
]
