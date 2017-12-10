# -*- coding: utf8 -*-
from __future__ import unicode_literals
import os
import re
import logging
import pdfkit
import datetime


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


def get_num_from_str(value):
    try:
        return int(re.sub(r'[^\d]*', '', value))
    except ValueError:
        return 0


def get_batch_logger():
    return logging.getLogger('revolution.management.commands')


def get_ap_logger():
    """営業システムのロガーを取得する。

    :return:
    """
    return logging.getLogger('area_parking')


def generate_pdf_from_string(text, out_path):
    logger = get_ap_logger()
    try:
        # config = pdfkit.configuration(wkhtmltopdf=r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe')
        # TODO: パスに日本語があったら、エラーになる。暫定対策：英語にしてから、また日本語名に変更する。
        options = {'encoding': "UTF-8"}
        # css = ['']
        pdfkit.from_string(text, out_path, options=options)
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


def get_report_format(self, filename):
    """各帳票フォーマットの格納場所を取得する。

    :param self:
    :param filename:
    :return:
    """
    prefix = 'reports/{}/'.format(self.parking_lot.name)
    return prefix + filename
