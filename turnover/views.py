import datetime

from utils.django_base import BaseTemplateView


# Create your views here.
class BalanceView(BaseTemplateView):
    template_name = 'turnover/balance.html'


class RequestMonthlyView(BaseTemplateView):
    template_name = 'turnover/request_monthly.html'

    def get_context_data(self, **kwargs):
        context = super(RequestMonthlyView, self).get_context_data(**kwargs)

        context.update({
            'year': '%04d' % datetime.date.today().year,
            'month': '%02d' % datetime.date.today().month,
        })
        return context
