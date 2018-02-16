# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import os

from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from django.template import Context, Template

from utils import constants, common
from utils.django_base import BaseModel
from utils.mail import EbMail

logger = common.get_ap_logger()


# Create your models here.
class Config(BaseModel):
    group = models.CharField(max_length=50, verbose_name="グループ")
    name = models.CharField(max_length=50, unique=True, verbose_name="設定名")
    value = models.CharField(max_length=2000, verbose_name="設定値")
    comment = models.TextField(max_length=255, blank=True, null=True, verbose_name="備考")

    class Meta:
        ordering = ['group', 'name']
        verbose_name = verbose_name_plural = "システム設定"
        db_table = 'mst_config'

    def __str__(self):
        return self.name

    @classmethod
    def get_value_by_name(cls, group, name, default_value=None):
        try:
            value = Config.objects.get(ame=name).value
            return value
        except ObjectDoesNotExist:
            if default_value:
                Config.objects.create(group=group, name=name, value=default_value)
            return default_value

    @classmethod
    def get_circle_radius(cls):
        """地図時で円作成時の半径を取得する。

        取得失敗の場合はデフォルトの2000メートルを返却する。

        :return:
        """
        default = 2000
        try:
            circle = Config.objects.get(name=constants.CONFIG_CIRCLE_RADIUS).value
            try:
                return int(circle)
            except Exception as ex:
                logger.error(ex)
                return default
        except ObjectDoesNotExist:
            Config.objects.create(group=constants.CONFIG_GROUP_SYSTEM, name=constants.CONFIG_CIRCLE_RADIUS,
                                  value=default)
            return default

    @classmethod
    def get_domain_name(cls):
        default = 'http://ap.mopa.jp'
        try:
            return Config.objects.get(name=constants.CONFIG_DOMAIN_NAME).value
        except ObjectDoesNotExist:
            Config.objects.create(group=constants.CONFIG_GROUP_SYSTEM, name=constants.CONFIG_DOMAIN_NAME,
                                  value=default)
            return default

    @classmethod
    def get_page_size(cls):
        """

        :return:
        """
        default = 25
        try:
            value = Config.objects.get(name=constants.CONFIG_PAGE_SIZE).value
            try:
                return int(value)
            except Exception as ex:
                logger.error(ex)
                return default
        except ObjectDoesNotExist:
            Config.objects.create(group=constants.CONFIG_GROUP_SYSTEM, name=constants.CONFIG_PAGE_SIZE, value=default)
            return default

    @classmethod
    def get_decimal_type(cls):
        """小数の処理区分を取得する。

        :return:
        """
        default = '0'
        try:
            return Config.objects.get(name=constants.CONFIG_DECIMAL_TYPE).value
        except ObjectDoesNotExist:
            Config.objects.create(group=constants.CONFIG_GROUP_SYSTEM, name=constants.CONFIG_DECIMAL_TYPE,
                                  value=default)
            return default

    @classmethod
    def get_consumption_tax_rate(cls):
        """消費税の税率を取得する。

        :return:
        """
        default = 0.08
        try:
            value = Config.objects.get(name=constants.CONFIG_CONSUMPTION_TAX_RATE).value
            try:
                return float(value)
            except Exception as ex:
                logger.error(ex)
                return default
        except ObjectDoesNotExist:
            Config.objects.create(group=constants.CONFIG_GROUP_SYSTEM, name=constants.CONFIG_CONSUMPTION_TAX_RATE,
                                  value=default)
            return default

    @classmethod
    def get_car_length_adjust(cls):
        """車全長の調整値。

        :return:
        """
        default = 0
        try:
            value = Config.objects.get(name=constants.CONFIG_CAR_LENGTH_ADJUST).value
            try:
                return int(value)
            except Exception as ex:
                logger.error(ex)
                return default
        except ObjectDoesNotExist:
            Config.objects.create(group=constants.CONFIG_GROUP_ADJUST_SIZE, name=constants.CONFIG_CAR_LENGTH_ADJUST,
                                  value=default)
            return default

    @classmethod
    def get_car_width_adjust(cls):
        """車全幅の調整値。

        :return:
        """
        default = 0
        try:
            value = Config.objects.get(name=constants.CONFIG_CAR_WIDTH_ADJUST).value
            try:
                return int(value)
            except Exception as ex:
                logger.error(ex)
                return default
        except ObjectDoesNotExist:
            Config.objects.create(group=constants.CONFIG_GROUP_ADJUST_SIZE, name=constants.CONFIG_CAR_WIDTH_ADJUST,
                                  value=default)
            return default

    @classmethod
    def get_car_height_adjust(cls):
        """車全高の調整値。

        :return:
        """
        default = 0
        try:
            value = Config.objects.get(name=constants.CONFIG_CAR_HEIGHT_ADJUST).value
            try:
                return int(value)
            except Exception as ex:
                logger.error(ex)
                return default
        except ObjectDoesNotExist:
            Config.objects.create(group=constants.CONFIG_GROUP_ADJUST_SIZE, name=constants.CONFIG_CAR_HEIGHT_ADJUST,
                                  value=default)
            return default

    @classmethod
    def get_car_weight_adjust(cls):
        """車重量の調整値。

        :return:
        """
        default = 0
        try:
            value = Config.objects.get(name=constants.CONFIG_CAR_WEIGHT_ADJUST).value
            try:
                return int(value)
            except Exception as ex:
                logger.error(ex)
                return default
        except ObjectDoesNotExist:
            Config.objects.create(group=constants.CONFIG_GROUP_ADJUST_SIZE, name=constants.CONFIG_CAR_WEIGHT_ADJUST,
                                  value=default)
            return default

    @classmethod
    def get_url_timeout(cls):
        """ＵＲＬのタイムアウト時間を取得する

        設定値の単位は時間ですけど、秒の値を戻す。

        :return:
        """
        default = 3600 * 24
        try:
            value = Config.objects.get(name=constants.CONFIG_URL_TIMEOUT).value
            try:
                return int(float(value) * 3600)
            except Exception as ex:
                logger.error(ex)
                return default
        except ObjectDoesNotExist:
            Config.objects.create(group=constants.CONFIG_GROUP_SYSTEM, name=constants.CONFIG_URL_TIMEOUT, value=24)
            return default

    @classmethod
    def get_gcm_url(cls):
        default = 'https://fcm.googleapis.com/fcm/send'
        try:
            return Config.objects.get(name=constants.CONFIG_GCM_URL).value
        except ObjectDoesNotExist:
            Config.objects.create(group=constants.CONFIG_GROUP_SYSTEM, name=constants.CONFIG_GCM_URL, value=default)
            return default

    @classmethod
    def get_firebase_serverkey(cls):
        default = ''
        try:
            return Config.objects.get(name=constants.CONFIG_FIREBASE_SERVERKEY).value
        except ObjectDoesNotExist:
            Config.objects.create(group=constants.CONFIG_GROUP_SYSTEM, name=constants.CONFIG_FIREBASE_SERVERKEY,
                                  value=default)
            return default

    @classmethod
    def get_google_map_key(cls):
        default = ''
        try:
            return Config.objects.get(name=constants.CONFIG_GOOGLE_MAP_KEY).value
        except ObjectDoesNotExist:
            Config.objects.create(group=constants.CONFIG_GROUP_GOOGLE, name=constants.CONFIG_GOOGLE_MAP_KEY,
                                  value=default)
            return default

    @classmethod
    def get_parking_lot_key_alert_percent(cls):
        """駐車場の残り鍵警告比率

        :return:
        """
        default = 0.3
        try:
            value = cls.get_value_by_name(
                constants.CONFIG_GROUP_SYSTEM, constants.CONFIG_PARKING_LOT_KEY_ALERT_PERCENT, default_value=default
            )
            return float(value)
        except Exception as ex:
            logger.error(ex)
            return default


class Company(BaseModel):
    name = models.CharField(unique=True, max_length=30, verbose_name="会社名")
    kana = models.CharField(blank=True, null=True, max_length=30, verbose_name="フリカナ")
    president = models.CharField(blank=True, null=True, max_length=30, verbose_name="代表者名")
    post_code = models.CharField(blank=True, null=True, max_length=8, verbose_name="郵便番号")
    address1 = models.CharField(blank=True, null=True, max_length=200, verbose_name="住所１")
    address2 = models.CharField(blank=True, null=True, max_length=200, verbose_name="住所２")
    tel = models.CharField(blank=True, null=True, max_length=15, verbose_name="電話番号",
                           validators=(RegexValidator(regex=constants.REG_TEL),))
    fax = models.CharField(blank=True, null=True, max_length=15, verbose_name="ファックス",
                           validators=(RegexValidator(regex=constants.REG_TEL),))
    email = models.EmailField(blank=True, null=True, verbose_name="メール")

    class Meta:
        db_table = 'ap_company'
        verbose_name = verbose_name_plural = "自社情報"

    def __str__(self):
        return self.name

    @classmethod
    def get_company(cls):
        """自社情報を取得する。

        :return:
        """
        return Company.objects.public_all().first()


class CarMaker(BaseModel):
    name = models.CharField(max_length=50, unique=True, verbose_name="メーカー")

    class Meta:
        db_table = 'mst_car_maker'
        ordering = ['name']
        verbose_name = "メーカー"
        verbose_name_plural = "メーカー一覧"

    def __str__(self):
        return self.name


class CarModel(BaseModel):
    maker = models.ForeignKey(CarMaker, on_delete=models.PROTECT, verbose_name="メーカー")
    name = models.CharField(max_length=100, verbose_name="車種")
    grade_name = models.CharField(max_length=100, blank=True, null=True, verbose_name="グレード名")
    sale_date = models.DateField(blank=True, null=True, verbose_name="発売年度")
    length = models.IntegerField(blank=False, null=True, verbose_name="全長")
    width = models.IntegerField(blank=False, null=True, verbose_name="全幅")
    height = models.IntegerField(blank=False, null=True, verbose_name="全高")
    weight = models.IntegerField(blank=False, null=True, verbose_name="重量")
    f_value = models.IntegerField(blank=False, null=True, verbose_name="F値")
    r_value = models.IntegerField(blank=False, null=True, verbose_name="R値")
    min_height = models.IntegerField(blank=False, null=True, verbose_name="ﾒｰｶｰの地上最低高")

    class Meta:
        db_table = 'mst_car_model'
        ordering = ['name']
        unique_together = ('maker', 'name', 'grade_name')
        verbose_name = "車種"
        verbose_name_plural = "車種一覧"

    def __str__(self):
        if self.grade_name:
            return '%s - %s ' % (self.name, self.grade_name)
        else:
            return self.name


class Bank(BaseModel):
    code = models.CharField(max_length=4, verbose_name="金融機関コード")
    name = models.CharField(max_length=30, verbose_name="金融機関名称")
    kana = models.CharField(blank=True, null=True, max_length=30, verbose_name="金融機関カナ")

    class Meta:
        db_table = 'mst_bank'
        ordering = ['code']
        verbose_name = "金融機関"
        verbose_name_plural = "金融機関一覧"

    def __str__(self):
        return self.name


class BankAccount(BaseModel):
    bank = models.ForeignKey(Bank, verbose_name="銀行")
    branch_no = models.CharField(max_length=7, verbose_name="支店番号")
    branch_name = models.CharField(max_length=20, verbose_name="支店名称")
    account_type = models.CharField(max_length=1, choices=constants.CHOICE_BANK_ACCOUNT_TYPE, verbose_name="預金種類")
    account_number = models.CharField(max_length=7, verbose_name="口座番号")
    account_holder = models.CharField(blank=True, null=True, max_length=30, verbose_name="口座名義")

    class Meta:
        db_table = 'mst_bank_account'
        ordering = ['bank', 'branch_no']
        unique_together = ('branch_no', 'account_number')
        verbose_name = "銀行口座"
        verbose_name_plural = "銀行口座一覧"

    def __str__(self):
        return self.branch_no


class TransmissionRoute(BaseModel):
    name = models.CharField(max_length=50, unique=True, verbose_name="名称")
    price_kbn = models.CharField(max_length=2, blank=True, null=True, verbose_name="金額区分",
                                 choices=constants.CHOICE_PRICE_KBN)

    class Meta:
        db_table = 'mst_transmission_route'
        ordering = ['id']
        verbose_name = "媒体"
        verbose_name_plural = "媒体一覧"

    def __str__(self):
        return self.name


class Mediation(BaseModel):
    name = models.CharField(max_length=50, unique=True, verbose_name="業者名称")

    class Meta:
        db_table = 'mst_mediation'
        ordering = ['name']
        verbose_name = "仲介業者"
        verbose_name_plural = "仲介業者一覧"

    def __str__(self):
        return self.name


class Payment(BaseModel):
    name = models.CharField(max_length=30, unique=True, verbose_name="入金項目")
    timing = models.CharField(max_length=2, choices=constants.CHOICE_PAY_TIMING, verbose_name="タイミング")
    amount = models.IntegerField(blank=True, null=True, verbose_name="デフォールト金額")
    consumption_tax_kbn = models.CharField(max_length=1, default=1, choices=constants.CHOICE_TAX_KBN,
                                           verbose_name="消費税")
    is_initial = models.BooleanField(default=False, verbose_name="初期作成")
    is_active = models.BooleanField(default=True, verbose_name="有効")
    comment = models.CharField(max_length=255, blank=True, null=True, verbose_name="備考")

    class Meta:
        db_table = 'mst_payment'
        ordering = ['timing', 'name']
        verbose_name = "入金項目"
        verbose_name_plural = "入金項目一覧"

    def __str__(self):
        return self.name

    def get_consumption_tax(self, amount=None):
        """消費税を取得する。

        :param amount:
        :return:
        """
        amount = amount if amount else self.amount
        if not amount:
            return 0
        if self.consumption_tax_kbn == '1':
            rate = Config.get_consumption_tax_rate()
            # 税抜の場合
            return common.get_consumption_tax(amount, rate, Config.get_decimal_type())
        else:
            return 0


class ReportFormat(BaseModel):
    path = models.FileField(upload_to=common.get_parking_lot_doc_path)
    kbn = models.CharField(max_length=3, choices=constants.CHOICE_REPORT_KBN, verbose_name="帳票区分")
    comment = models.CharField(max_length=255, blank=True, null=True, verbose_name="備考")
    order = models.SmallIntegerField(editable=False, verbose_name="並び順")

    class Meta:
        db_table = 'mst_report_format'
        ordering = ['kbn']
        verbose_name = "帳票フォーマット"
        verbose_name_plural = "帳票フォーマット一覧"

    def __str__(self):
        return os.path.basename(str(self.path))


class MailTemplate(BaseModel):
    title = models.CharField(max_length=50, verbose_name="送信メールのタイトル")
    body = models.TextField(verbose_name="メール本文")
    password = models.TextField(blank=True, null=True, verbose_name="パスワードお知らせ本文")
    comment = models.CharField(max_length=255, blank=True, null=True, verbose_name="説明")

    class Meta:
        db_table = 'mst_mail_template'
        ordering = ['title']
        verbose_name = verbose_name_plural = "メールテンプレート"

    def __str__(self):
        return self.title


class MailGroup(BaseModel):
    code = models.CharField(max_length=3, primary_key=True, choices=constants.CHOICE_MAIL_GROUP, verbose_name="コード")
    name = models.CharField(max_length=50, blank=False, null=True, verbose_name="名称")
    sender = models.EmailField(verbose_name="メール差出人")
    template = models.ForeignKey(MailTemplate, on_delete=models.CASCADE, verbose_name="メールテンプレート")

    class Meta:
        db_table = 'mst_mail_group'
        ordering = ['code']
        verbose_name = verbose_name_plural = "メールグループ"

    def __str__(self):
        return self.name

    def get_cc_list(self):
        """メール送信時のＣＣ一覧を取得する。

        :return:
        """
        return MailCcList.objects.public_filter(group=self, is_bcc=False)

    def get_bcc_list(self):
        """メール送信時のＢＣＣ一覧を取得する。

        :return:
        """
        return MailCcList.objects.public_filter(group=self, is_bcc=True)

    @classmethod
    def get_subscription_send_group(cls):
        """ユーザー申込み時のメール送信に関する情報を取得する。

        :return:
        """
        try:
            return MailGroup.objects.get(code='010')
        except ObjectDoesNotExist:
            return None

    @classmethod
    def get_subscription_completed_group(cls):
        """ユーザー申込み完了時のメール送信に関する情報を取得する。

        :return:
        """
        try:
            return MailGroup.objects.get(code='011')
        except ObjectDoesNotExist:
            return None

    @classmethod
    def get_inspection_send_group(cls):
        """審査用フォーム送付時のメール送信に関する情報を取得する。

        :return:
        """
        try:
            return MailGroup.objects.get(code='012')
        except ObjectDoesNotExist:
            return None

    @classmethod
    def get_inspection_completed_group(cls):
        """審査用フォーム完了時のメール送信に関する情報を取得する。

        :return:
        """
        try:
            return MailGroup.objects.get(code='013')
        except ObjectDoesNotExist:
            return None

    @classmethod
    def get_contract_form_send_group(cls):
        """ユーザー契約時のメール送信に関する情報を取得する。

        :return:
        """
        try:
            return MailGroup.objects.get(code='040')
        except ObjectDoesNotExist:
            return None

    @classmethod
    def get_contract_form_completed_group(cls):
        """ユーザー契約完了時のメール送信に関する情報を取得する。

        :return:
        """
        try:
            return MailGroup.objects.get(code='041')
        except ObjectDoesNotExist:
            return None

    @classmethod
    def get_contract_send_group(cls):
        """ユーザー契約時のメール送信に関する情報を取得する。

        :return:
        """
        try:
            return MailGroup.objects.get(code='042')
        except ObjectDoesNotExist:
            return None

    @classmethod
    def get_contract_other_send_group(cls):
        """ユーザー契約時のメール送信に関する情報を取得する。

        :return:
        """
        try:
            return MailGroup.objects.get(code='060')
        except ObjectDoesNotExist:
            return None

    @classmethod
    def get_contract_cancellation_send_group(cls):
        """ユーザー解約時のメール送信に関する情報を取得する。

        :return:
        """
        try:
            return MailGroup.objects.get(code='310')
        except ObjectDoesNotExist:
            return None

    @classmethod
    def get_parking_lot_cancellation_send_group(cls):
        """物件解約時のメール送信に関する情報を取得する。

        :return:
        """
        try:
            return MailGroup.objects.get(code='322')
        except ObjectDoesNotExist:
            return None

    @classmethod
    def get_batch_key_alert_group(cls):
        """駐車場の予備鍵数が足り場合のメール送信設定を取得する。

        :return:
        """
        try:
            return MailGroup.objects.get(code='800')
        except ObjectDoesNotExist:
            return None


    def get_template_content(self, context):
        """メールテンプレートの内容を取得する。

        :param context:
        :return:
        """
        t_title = Template(self.template.title)
        t_body = Template(self.template.body)
        t_password = Template(self.template.password) if self.template.password else None
        comment = self.template.comment or ''
        ctx = Context(context)
        return {
            'title': t_title.render(ctx),
            'body': t_body.render(ctx),
            'password': t_password.render(ctx) if t_password else '',
            'comment': comment,
        }

    def send_main(self, recipient_list, context):
        """メール送信する

        :param context:
        :return:
        """
        content = self.get_template_content(context)
        mail_data = {
            'sender': self.sender,
            'recipient_list': recipient_list,
            'cc_list': [cc.email for cc in self.get_cc_list()],
            'bcc_list': [bcc.email for bcc in self.get_bcc_list()],
            'mail_title': content.get('title'),
            'mail_body': content.get('body'),
        }

        mail = EbMail(**mail_data)
        mail.send_email()


class MailCcList(BaseModel):
    group = models.ForeignKey(MailGroup, on_delete=models.CASCADE, verbose_name="メールグループ")
    email = models.EmailField(verbose_name="メールアドレス")
    is_bcc = models.BooleanField(default=False, verbose_name="ＢＣＣ")

    class Meta:
        db_table = 'mst_mail_cc'
        ordering = ['group', 'email']
        verbose_name = verbose_name_plural = "メールＣＣリスト"

    def __str__(self):
        return self.email


class BatchManage(BaseModel):
    name = models.CharField(max_length=50, unique=True, verbose_name="バッチＩＤ")
    title = models.CharField(max_length=50, verbose_name="タイトル")
    cron_tab = models.CharField(blank=True, null=True, max_length=100, verbose_name="実行タイミング")
    is_active = models.BooleanField(default=True, verbose_name="有効フラグ")
    comment = models.CharField(blank=True, null=True, max_length=255, verbose_name="説明")

    class Meta:
        db_table = 'mst_batch_manage'
        verbose_name = "バッチ管理"
        verbose_name_plural = "バッチ管理"

    def __str__(self):
        return self.title

    def get_logger(self):
        """バッチのロガーを取得する。

        :return:
        """
        return common.get_batch_logger(self.name)

    @classmethod
    def get_log_entry_user(cls, username='batch'):
        """ログエントリーにログを記録するにはログインユーザが必要

        :return:
        """
        try:
            user = User.objects.get(username=username)
            return user
        except ObjectDoesNotExist:
            try:
                user = User.objects.get(username='admin')
                return user
            except ObjectDoesNotExist:
                return None

    @classmethod
    def get_batch_by_name(cls, name):
        """指定した名前のバッチを取得する。

        :param name:
        :return:
        """
        try:
            batch = BatchManage.objects.get(name=name)
        except ObjectDoesNotExist:
            batch = BatchManage(name=name)
        return batch


class PushNotification(BaseModel):
    user = models.ForeignKey(User, verbose_name="ユーザー")
    registration_id = models.CharField(max_length=1000, verbose_name="デバイスの登録ＩＤ")
    key_auth = models.CharField(max_length=100)
    key_p256dh = models.CharField(max_length=256)
    title = models.CharField(blank=True, null=True, max_length=100)
    message = models.CharField(blank=True, null=True, max_length=256)
    url = models.URLField(blank=True, null=True)

    class Meta:
        db_table = 'ap_push_notification'
        verbose_name = "通知デバイス"
        verbose_name_plural = "通知デバイス一覧"

    def __str__(self):
        return self.registration_id
