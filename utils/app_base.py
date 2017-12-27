import datetime
import json
import requests
from urllib.parse import urljoin

from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from django.core.signing import TimestampSigner
from django.urls import reverse

from master.models import Company, Config, Payment, PushNotification


def get_total_context(parking_lot=None, contractor=None, subscription=None):
    context = get_company_context()
    if parking_lot:
        context.update(get_parking_lot_context(parking_lot))
    if contractor:
        context.update(get_contractor_context(contractor))
    if subscription:
        context.update(get_subscription_context(subscription))

    context.update({
        'current_date': datetime.date.today(),
    })
    payment = get_receipt_payment()
    if payment:
        context.update({
            'receipt_amount': payment.amount,
            'receipt_without_consumption': payment.consumption_tax_kbn == '1',
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


def get_subscription_context(subscription):
    """テンプレートに出力する契約者の情報

    :param contractor:
    :return:
    """
    if subscription:
        return {
            'user_name': subscription.name,
            'user_tel': subscription.tel,
            'user_fax': subscription.fax,
            'user_email': subscription.email,
            'user_address1': subscription.address1,
            'user_address2': subscription.address2,
        }
    else:
        return dict()


def get_user_subscription_url(task):
    url = reverse('format:user_subscription_step1', kwargs={'signature': task.get_signed_pk()})
    domain_name = Config.get_domain_name()
    return {'user_subscription_url': urljoin(domain_name, url)}


def get_receipt_payment():
    """保管場所承諾証明書発行手数料

    :param contract:
    :return:
    """
    try:
        return Payment.objects.get(timing=41)
    except (ObjectDoesNotExist, MultipleObjectsReturned):
        return None


def get_signed_value(key, salt=None):
    """

    :param key:
    :param salt:
    :return:
    """
    signer = TimestampSigner(salt=salt)
    return signer.sign(key)


def get_unsigned_value(signature, salt=None):
    """

    :param signature:
    :param salt:
    :return:
    """
    signer = TimestampSigner(salt=salt)
    timeout = Config.get_url_timeout()
    return signer.unsign(signature, max_age=datetime.timedelta(seconds=timeout))


def push_notification(users, title, message, gcm_url=None):
    """プッシュ通知を各端末に送信する。

    :param users:
    :param title:
    :param message:
    :param gcm_url:
    :return:
    """
    if not gcm_url:
        gcm_url = Config.get_gcm_url()

    queryset = PushNotification.objects.public_filter(user__in=users)
    queryset.update(title=title, message=message)
    for notification in queryset:
        headers = {
            'content-type': 'application/json',
            'Authorization': "key=" + Config.get_firebase_serverkey(),
            'Encryption': 'salt=' + notification.key_auth,
            'Crypto-Key': 'dh=' + notification.key_p256dh,
            'Content-Encoding': 'aesgcm'
        }
        # 渡すデータは適当です。
        # dictのkeyはAndroidのextrasのkeyと合わせましょう
        params = {
            'to': notification.registration_id,
            "data": {
                "title": u"メッセージタイトル",
                "body": u"メッセージ本文"
            },
            "notification": {
                "title": u"メッセージタイトル",
                "body": u"メッセージ本文"
            },
        }

        requests.post(gcm_url, data=json.dumps(params), headers=headers)
