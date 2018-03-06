from django.conf.urls import url

from . import views

urlpatterns = [
    url('^balance.html$', views.BalanceView.as_view(), name='balance'),
    url('^request_monthly.html$', views.RequestMonthlyView.as_view(), name='request_monthly'),
    url('^daily_income.html$', views.DailyIncomeView.as_view(), name='daily_income')
]
