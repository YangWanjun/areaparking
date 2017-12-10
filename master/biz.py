from django.core.exceptions import ObjectDoesNotExist

from . import models


def get_subscription_mail_info():
    """ユーザー申込み時のメール送信に関する情報を取得する。

    :return:
    """
    try:
        return models.MailGroup.objects.get(code='001')
    except ObjectDoesNotExist:
        return None