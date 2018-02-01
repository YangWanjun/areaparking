from django.shortcuts import redirect

from . import models
from utils.django_base import BaseModelViewSet, BaseView


# Create your views here.
class Index(BaseView):

    def get(self, request, *args, **kwargs):
        return redirect('management_dep:vbankaccount_list')


class VBankAccountViewSet(BaseModelViewSet):
    model = models.VBankAccount
    list_display = ('bank', 'branch_name', 'account_number', 'contractor', 'parking_lot', 'parking_position', 'status')
    list_display_links = ('account_number',)

    def has_change_permission(self, request, obj=None):
        return False
