from django.shortcuts import redirect

from utils.django_base import BaseView, BaseTemplateView


# Create your views here.
class Index(BaseView):

    def get(self, request, *args, **kwargs):
        return redirect('billing:import_transfer')


class ImportTransfer(BaseTemplateView):
    template_name = 'billing/import_transfer.html'

    def get_context_data(self, **kwargs):
        context = super(ImportTransfer, self).get_context_data(**kwargs)
        return context
