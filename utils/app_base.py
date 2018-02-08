import datetime
import json
import requests
from urllib.parse import urljoin

from django.contrib.humanize.templatetags import humanize
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from django.core.signing import TimestampSigner
from django.urls import reverse

from . import common
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
    """テンプレートに出力する申込者の情報

    :param subscription:
    :return:
    """
    if subscription:
        data = {
            'user_name': subscription.name or '',
            'user_kana': subscription.kana or '',
            'user_tel': subscription.tel or '',
            'user_fax': subscription.fax or '',
            'user_email': subscription.email or '',
            'user_address1': subscription.address1 or '',
            'user_address2': subscription.address2 or '',
            'car_maker': subscription.car_maker or '',
            'car_model': subscription.car_model or '',
            'car_no_plate': subscription.car_no_plate or '',
            'car_length': humanize.intcomma(subscription.car_length) if subscription.car_length else '',
            'car_width': humanize.intcomma(subscription.car_width) if subscription.car_width else '',
            'car_height': humanize.intcomma(subscription.car_height) if subscription.car_height else '',
            'car_weight': humanize.intcomma(subscription.car_weight) if subscription.car_weight else '',
            'contract_start_date': subscription.contract_start_date or '',
            'contract_end_month': subscription.contract_end_month or '',
        }
        if subscription.category == '1':
            # 個人の場合
            data.update({
                'personal_kana': subscription.kana or '',
                'personal_name': subscription.name or '',
                'personal_tel': subscription.tel or '',
                'personal_birthday': subscription.personal_birthday or '',
                'personal_post_code1': subscription.post_code1 or '',
                'personal_post_code2': subscription.post_code2 or '',
                'personal_address1': subscription.address1 or '',
                'personal_address2': subscription.address2 or '',
                'personal_phone': subscription.personal_phone or '',
                'personal_email': subscription.email or '',
                'workplace_name': subscription.workplace_name or '',
                'workplace_post_code1': subscription.workplace_post_code1 or '',
                'workplace_post_code2': subscription.workplace_post_code2 or '',
                'workplace_address1': subscription.workplace_address1 or '',
                'workplace_address2': subscription.workplace_address2 or '',
                'workplace_tel': subscription.workplace_tel or '',
                'workplace_fax': subscription.workplace_fax or '',
                'personal_contact_name': subscription.contact_name or '',
                'personal_contact_tel': subscription.contact_tel or '',
                'personal_contact_relation': subscription.contact_relation or '',
            })
        else:
            # 法人の場合
            data.update({
                'corporate_kana': subscription.kana or '',
                'corporate_name': subscription.name or '',
                'corporate_tel': subscription.tel or '',
                'corporate_fax': subscription.fax or '',
                'corporate_president': subscription.corporate_president or '',
                'corporate_post_code1': subscription.post_code1 or '',
                'corporate_post_code2': subscription.post_code2 or '',
                'corporate_address1': subscription.address1 or '',
                'corporate_address2': subscription.address2 or '',
                'corporate_business_type': subscription.corporate_business_type or '',
                'corporate_staff_kana': subscription.corporate_staff_kana or '',
                'corporate_staff_name': subscription.corporate_staff_name or '',
                'corporate_staff_email': subscription.corporate_staff_email or '',
                'corporate_staff_tel': subscription.corporate_staff_tel or '',
                'corporate_staff_fax': subscription.corporate_staff_fax or '',
                'corporate_staff_phone': subscription.corporate_staff_phone or '',
                'corporate_contact_name': subscription.contact_name or '',
                'corporate_contact_tel': subscription.contact_tel or '',
                'corporate_contact_relation': subscription.contact_relation or '',
                'corporate_user_kana': subscription.corporate_user_kana or '',
                'corporate_user_name': subscription.corporate_user_name or '',
                'corporate_user_tel': subscription.corporate_user_tel or '',
                'corporate_user_address1': subscription.corporate_user_address1 or '',
            })
        return data
    else:
        return dict()


def get_user_subscription_simple_url(task):
    """ユーザー申込時のURLを取得する。

    :param task:
    :return:
    """
    subscription = task.process.content_object
    url = reverse('format:user_subscription_simple_step1', kwargs={'signature': get_signed_value(subscription.pk)})
    domain_name = Config.get_domain_name()
    return {'user_subscription_simple_url': urljoin(domain_name, url)}


def get_user_subscription_url(task):
    """ユーザー申込時のURLを取得する。

    :param task:
    :return:
    """
    subscription = task.process.content_object
    url = reverse('format:user_subscription_step1', kwargs={'signature': get_signed_value(subscription.pk)})
    domain_name = Config.get_domain_name()
    return {'user_subscription_url': urljoin(domain_name, url)}


def get_user_contract_url(task):
    """ユーザー契約時のURLを取得する。

    :param task:
    :return:
    """
    subscription = task.process.content_object
    url = reverse('format:user_contract_step1', kwargs={'signature': get_signed_value(subscription.pk)})
    domain_name = Config.get_domain_name()
    return {'user_contract_url': urljoin(domain_name, url)}


def get_contract_cancellation_url(task):
    """ユーザー解約時のURLを取得する。

    :param task:
    :return:
    """
    subscription = task.process.content_object
    url = reverse('format:user_contract_cancellation_step1', kwargs={'signature': get_signed_value(subscription.pk)})
    domain_name = Config.get_domain_name()
    return {'user_cancellation_url': urljoin(domain_name, url)}


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


def push_notification(users, title, message, url=None, gcm_url=None):
    """プッシュ通知を各端末に送信する。

    :param users:
    :param title:
    :param message:
    :param gcm_url:
    :return:
    """
    if not gcm_url:
        gcm_url = Config.get_gcm_url()

    if users:
        queryset = PushNotification.objects.public_filter(user__in=users)
    else:
        queryset = PushNotification.objects.public_all()
    queryset.update(title=title, message=message, url=url)
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


def get_consumption_tax(amount):
    """消費税を取得する。

    :return:
    """
    if not amount:
        return 0
    rate = Config.get_consumption_tax_rate()
    return common.get_integer(amount * rate, Config.get_decimal_type())
