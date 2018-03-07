# -*- coding: utf8 -*-
from __future__ import unicode_literals
import os
import re
import calendar
import logging
import pdfkit
import datetime
import random
import math

from calendar import monthrange

from django.conf import settings

from . import constants
from .errors import CustomException


def get_root_path():
    """アプリのルートパスを取得する

    :return:
    """
    return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def get_data_path():
    """インポートするデータのパスを取得する。

    :return:
    """
    return os.path.join(get_root_path(), 'data')


def get_temp_path():
    """一時フォルダーを取得する。

    :return:
    """
    path = os.path.join(settings.MEDIA_ROOT, 'temp')
    if not os.path.exists(path):
        os.mkdir(path)
    return path


def get_user_subscription_path():
    path = os.path.join(settings.MEDIA_ROOT, 'user_subscription')
    if not os.path.exists(path):
        os.mkdir(path)
    return path


def get_temp_file(ext):
    """指定拡張子の一時ファイルを取得する。

    :param ext:
    :return:
    """
    temp_root = get_temp_path()
    file_name = "{0}_{1}.{2}".format(
        datetime.datetime.now().strftime('%Y%m%d%H%M%S%f'),
        random.randint(10000, 99999),
        ext
    )
    temp_file = os.path.join(temp_root, file_name)
    return temp_file


def get_num_from_str(value):
    try:
        return int(re.sub(r'[^\d]*', '', value))
    except ValueError:
        return 0


def is_number(string):
    """数字であるかどうかを判断する。

    :param string:
    :return:
    """
    if re.match(constants.REG_NUMBER, string):
        return True
    else:
        return False


def is_match(string, pattern):
    """

    :param string:
    :param pattern:
    :return:
    """
    return re.match(pattern, string)


def get_ap_logger():
    """営業システムのロガーを取得する。

    :return:
    """
    return logging.getLogger('area_parking')


def get_batch_logger(name):
    """バッチのロガーを取得する。

    :param name: バッチ名（ＩＤ）
    :return:
    """
    return logging.getLogger('batch.%s' % name)


def generate_pdf_from_string(html, out_path):
    logger = get_ap_logger()
    try:
        # config = pdfkit.configuration(wkhtmltopdf=r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe')
        # TODO: パスに日本語があったら、エラーになる。暫定対策：英語にしてから、また日本語名に変更する。
        options = {
            'encoding': "UTF-8",
            'page-size': 'A4',
            'dpi': 300,
        }
        # css = ['']
        pdfkit.from_string(html, out_path, options=options)
    except Exception as ex:
        logger.error(str(ex))


def get_parking_lot_image_path(self, filename):
    """駐車場に関する写真の格納場所を取得する。

    :param self:
    :param filename:
    :return:
    """
    prefix = 'images/'
    name = '{}_{}'.format(self.parking_lot.name, datetime.datetime.now().strftime('%y%m%d%H%M%S%f'))
    extension = os.path.splitext(filename)[-1]
    return prefix + name + extension


def get_parking_lot_doc_path(self, filename):
    """駐車場に関する書類の格納場所を取得する。

    :param self:
    :param filename:
    :return:
    """
    prefix = 'docs/{}/'.format(self.parking_lot.name)
    return prefix + filename


def get_report_path(self, filename):
    """帳票の格納場所を取得する。

    :param self:
    :param filename:
    :return:
    """
    new_name = filename
    prefix = ''
    content_object = self.content_object
    if content_object.__class__.__name__ == 'Subscription':
        prefix = 'user_subscription/'
        parking_lot = content_object.parking_lot
        ext = os.path.splitext(filename)[1]
        new_name = "{0}_{1}_{2}{3}".format(
            parking_lot.name,
            content_object.name,
            datetime.datetime.now().strftime('%Y%m%d%H%M%S%f'),
            ext
        )
    return prefix + new_name


def get_report_format(self, filename):
    """各帳票フォーマットの格納場所を取得する。

    :param self:
    :param filename:
    :return:
    """
    prefix = 'reports/{}/'.format(self.parking_lot.name)
    return prefix + filename


def get_days_by_month(date):
    """指定日付の月の日数を取得する。

    :param date:
    :return:
    """
    month, days = monthrange(date.year, date.month)
    return days


def get_integer(value, decimal_type):
    """小数がある場あるの処理方法

    :param value:
    :param decimal_type:
    :return:
    """
    if value:
        if decimal_type == '0':
            # 切り捨て
            return math.floor(value)
        elif decimal_type == '1':
            # 四捨五入
            return round(value)
        elif decimal_type == '2':
            # 切り上げ
            return math.ceil(value)
    else:
        return 0


def add_days(source_date, days=1):
    """指定日数後の日付を取得する。

    :param source_date:
    :param days:
    :return:
    """
    return source_date + datetime.timedelta(days=days)


def add_months(source_date, months=1):
    """指定月数後の日付を取得する

    :param source_date:
    :param months:
    :return:
    """
    month = source_date.month - 1 + months
    year = int(source_date.year + month / 12)
    month = month % 12 + 1
    day = min(source_date.day, calendar.monthrange(year, month)[1])
    return datetime.date(year, month, day)


def get_first_day_by_month(source_date):
    """指定日付の初日を取得する

    :param source_date:
    :return:
    """
    return datetime.date(source_date.year, source_date.month, 1)


def get_last_day_by_month(source_date):
    """指定日付の末尾を取得する

    :param source_date:
    :return:
    """
    next_month = add_months(source_date, 1)
    return next_month + datetime.timedelta(days=-next_month.day)


def date_handler(obj):
    """JSON serializable Support for date

    :param obj:
    :return:
    """
    return obj.isoformat() if hasattr(obj, 'isoformat') else obj


def json_default(o):
    return o.__dict__


def get_consumption_tax(amount, tax_rate, decimal_type):
    """消費税を取得する。

    :param amount:
    :param tax_rate:
    :param decimal_type:
    :return:
    """
    if not amount:
        return 0
    return get_integer(amount * tax_rate, decimal_type)


def get_choice_name_by_key(choices, key):
    """２次元のTupleからキーによって、名称を取得する。

    :param choices:
    :param key:
    :return:
    """
    if choices and key:
        if isinstance(choices, tuple):
            for k, v in choices:
                if k == key:
                    return v
    return ''


def to_half_size(ustring):
    """文字列を半角に変換する

    :param ustring:
    :return:
    """
    if not ustring:
        return ustring

    rstring = ""
    for uchar in ustring:
        inside_code = ord(uchar)
        if inside_code == 0x3000:
            # 全角スペース(0x3000)を半角スペース(0x0020)に変換
            inside_code = 0x0020
        else:
            inside_code -= 0xfee0
        if inside_code < 0x0020 or inside_code > 0x7e:
            rstring += uchar
        if inside_code > 0:
            rstring += chr(inside_code)
    return rstring


def to_full_size(ustring):
    """文字列を全角に変換する

    :param ustring:
    :return:
    """
    if not ustring:
        return ustring

    rstring = ""
    for uchar in ustring:
        inside_code = ord(uchar)
        if inside_code < 0x0020 or inside_code > 0x7e:
            rstring += uchar
        if inside_code == 0x0020:
            inside_code = 0x3000
        else:
            inside_code += 0xfee0
        rstring += chr(inside_code)
    return rstring


def get_continued_positions(string):
    """連続の車室番号を取得する。

    :param string:
    :return:
    """
    if is_match(string, constants.REG_CONTINUED_POSITIONS):
        m = re.search(constants.REG_CONTINUED_POSITIONS, string)
        start, end = m.groups()
        if int(start) > int(end):
            raise CustomException(constants.ERROR_PARKING_POSITION_RANGE)
        else:
            return list(range(int(start), int(end) + 1))
    else:
        return []


class Setting(object):
    __instance = None

    def __new__(cls, *args, **kwargs):
        if cls.__instance is None:
            cls.__instance = object.__new__(cls)
        return cls.__instance

    def __init__(self):
        self.email_address = None
        self.email_smtp_host = None
        self.email_smtp_port = None
        self.email_password = None
        self.circle_radius = None
        self.domain_name = None
        self.page_size = None
        self.decimal_type = None
        self.consumption_tax_rate = None
        self.car_length_adjust = None
        self.car_width_adjust = None
        self.car_height_adjust = None
        self.car_weight_adjust = None
        self.url_timeout = None
        self.gcm_url = None
        self.firebase_serverkey = None
        self.google_map_key = None
        self.parking_lot_key_alert_percent = None
