from django.conf.urls import url
from django.views import generic

from . import views


urlpatterns = [
    url('^$', generic.View.as_view(), name="index"),
    url('^url_timeout\.html$', views.UrlTimeoutView.as_view(), name='url_timeout'),
    # 申込み用フォーム(車室の一時確保に必要な項目)【個人・法人共通】
    url('^user_subscription_simple_step1/(?P<signature>[^/]+)\.html$', views.UserSubscriptionSimpleStep1View.as_view(),
        name="user_subscription_simple_step1"),
    url('^user_subscription_simple_step2/(?P<signature>[^/]+)\.html$', views.UserSubscriptionSimpleStep2View.as_view(),
        name="user_subscription_simple_step2"),
    # ユーザー申込み
    url('^user_subscription_step1/(?P<signature>[^/]+)\.html$', views.UserSubscriptionStep1View.as_view(),
        name="user_subscription_step1"),
    url('^user_subscription_step2/(?P<signature>[^/]+)\.html$', views.UserSubscriptionStep2View.as_view(),
        name="user_subscription_step2"),
    url('^user_subscription_step3/(?P<signature>[^/]+)\.html$', views.UserSubscriptionStep3View.as_view(),
        name="user_subscription_step3"),
    url('^user_subscription_step4/(?P<signature>[^/]+)\.html$', views.UserSubscriptionStep4View.as_view(),
        name="user_subscription_step4"),
    url('^user_subscription_step5/(?P<signature>[^/]+)\.html$', views.UserSubscriptionStep5View.as_view(),
        name="user_subscription_step5"),
    url('^subscription_confirm/(?P<subscription_id>\d+)/$',
        views.SubscriptionConfirmView.as_view(), name="report_subscription_confirm"),
    url('^subscription/(?P<subscription_id>\d+)/$',
        views.SubscriptionView.as_view(), name="report_subscription"),
    # ユーザー契約
    url('^user_contract_step1/(?P<signature>[^/]+)\.html$', views.UserContractStep1View.as_view(),
        name="user_contract_step1"),
    url('^user_contract_step2/(?P<signature>[^/]+)\.html$', views.UserContractStep2View.as_view(),
        name="user_contract_step2"),
    url('^user_contract_step3/(?P<signature>[^/]+)\.html$', views.UserContractStep3View.as_view(),
        name="user_contract_step3"),
    url('^user_contract_step4/(?P<signature>[^/]+)\.html$', views.UserContractStep4View.as_view(),
        name="user_contract_step4"),
    # 一般解約
    url('^user_contract_cancellation_step1/(?P<signature>[^/]+)\.html$', views.ContractCancellationStep1View.as_view(),
        name="user_contract_cancellation_step1"),
    url('^user_contract_cancellation_step2/(?P<signature>[^/]+)\.html$', views.ContractCancellationStep2View.as_view(),
        name="user_contract_cancellation_step2"),

    # Download PDF
    url('^download/pdf/subscription_confirm/(?P<subscription_id>\d+)/$',
        views.GenerateSubscriptionConfirmPdfView.as_view(), name='download_report_subscription_confirm'),
    url('^download/pdf/subscription/(?P<subscription_id>\d+)/$',
        views.GenerateSubscriptionPdfView.as_view(), name='download_report_subscription'),
]
