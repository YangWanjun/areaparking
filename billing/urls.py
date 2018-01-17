from django.conf.urls import url, include

from . import views


urlpatterns = [
    url('^$', views.Index.as_view(), name="index"),
    url('^import-transfer/', views.ImportTransfer.as_view(), name='import_transfer'),
    url('^arrears-list/', views.ArrearsListView.as_view(), name='arrears_list'),
    url('^transfer/', include(views.TransferViewSet().urls)),
]
