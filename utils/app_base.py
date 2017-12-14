import datetime
from urllib.parse import urljoin

from django.urls import reverse

from master.models import Company, Config


def get_total_context(parking_lot=None, contractor=None):
    context = get_company_context()
    if parking_lot:
        context.update(get_parking_lot_context(parking_lot))
    if contractor:
        context.update(get_contractor_context(contractor))

    context.update({
        'current_date': datetime.date.today(),
    })
    return context


def get_company_context():
    """テンプレートに出力する自社情報

    :return:
    """
    company = Company.get_company()
    if company:
        return {
            'company_name': company.name,
            'company_post_code': company.post_code or '',
            'company_address1': company.address1 or '',
            'company_address2': company.address2 or '',
            'company_tel': company.tel or '',
            'company_fax': company.fax or '',
            'company_email': company.email or '',
        }
    else:
        return dict()


def get_parking_lot_context(parking_lot):
    """テンプレートに出力する駐車場の情報

    :param parking_lot:
    :return:
    """
    if parking_lot:
        return {
            'parking_lot_name': parking_lot.name,
        }
    else:
        return dict()


def get_contractor_context(contractor):
    """テンプレートに出力する契約者の情報

    :param contractor:
    :return:
    """
    if contractor:
        return {
            'user_name': contractor.name,
            'user_tel': contractor.tel,
            'user_fax': contractor.fax,
            'user_email': contractor.email,
            'user_address1': contractor.address1,
            'user_address2': contractor.address2,
        }
    else:
        return dict()


def get_user_subscription_url(task):
    url = reverse('format:user_subscription', kwargs={'task_id': task.pk})
    domain_name = Config.get_domain_name()
    return {'user_subscription_url': urljoin(domain_name, url)}
