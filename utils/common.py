# -*- coding: utf8 -*-
from __future__ import unicode_literals
import os
import re
import logging
import pdfkit


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


def generate_pdf_from_string(text, out_path):
    try:
        # config = pdfkit.configuration(wkhtmltopdf=r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe')
        # TODO: パスに日本語があったら、エラーになる。暫定対策：英語にしてから、また日本語名に変更する。
        options = {'encoding': "UTF-8"}
        # css = ['']
        pdfkit.from_string(text, out_path, options=options)
    except Exception as ex:
        print unicode(ex)
