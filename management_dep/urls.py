from django.conf.urls import url, include

from . import views


urlpatterns = [
    url('^$', views.Index.as_view(), name="index"),
    url('^bank-account/', include(views.VBankAccountViewSet().urls)),
]
