# -*- coding: utf8 -*-
from __future__ import unicode_literals
import os
import re
import logging


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
