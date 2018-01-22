from django.conf.urls import url, include

from . import views


urlpatterns = [
    url('^$', views.Index.as_view(), name="index"),
    url('^import-transfer/', views.ImportTransfer.as_view(), name='import_transfer'),
    # url('^arrears-list/', views.ArrearsListView.as_view(), name='arrears_list'),
    url('^arrears/', include(views.ArrearsViewSet().urls)),
    url('^transfer/', include(views.TransferViewSet().urls)),
    url('^contractor/', include(views.ContractorVewSet().urls)),
    url('^parking-lot/', include(views.ParkingLotViewSet().urls)),
]
