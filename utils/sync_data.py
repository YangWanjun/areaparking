# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import os
import xlrd
import datetime

import common

from django.core.exceptions import ObjectDoesNotExist

from master.models import CarModel, CarMaker


def sync_car_models():
    path = os.path.join(common.get_data_path(), '自動車一覧.xls')
    if os.path.exists(path):
        book = xlrd.open_workbook(path)
        sheet = book.sheet_by_index(0)
        for row in range(sheet.nrows):
            if row == 0:
                continue
            maker_name = sheet.cell(row, 0).value
            name = sheet.cell(row, 1).value
            grade_name = sheet.cell(row, 2).value
            try:
                maker = CarMaker.objects.get(name=maker_name)
            except ObjectDoesNotExist:
                maker = CarMaker(name=maker_name)
                maker.save()
            try:
                model = CarModel.objects.get(maker=maker, name=name, grade_name=grade_name)
            except Exception:
                model = CarModel(maker=maker, name=name, grade_name=grade_name)
            try:
                model.sale_date = datetime.datetime.strptime(sheet.cell(row, 7).value.encode('utf8'), "%Y年%m月%d日".encode('utf8'))
            except Exception as ex:
                print unicode(ex), sheet.cell(row, 7).value
            try:
                    model.length = common.get_num_from_str(sheet.cell(row, 29).value)
            except Exception as ex:
                print unicode(ex), sheet.cell(row,29).value
            try:
                model.width = common.get_num_from_str(sheet.cell(row, 30).value)
            except Exception as ex:
                print unicode(ex), sheet.cell(row, 30).value
            try:
                model.height = common.get_num_from_str(sheet.cell(row, 31).value)
            except Exception as ex:
                print unicode(ex), sheet.cell(row, 31).value
            try:
                model.weight = common.get_num_from_str(sheet.cell(row, 17).value)
            except Exception as ex:
                print unicode(ex), sheet.cell(row, 17).value
            try:
                model.min_height = common.get_num_from_str(sheet.cell(row, 33).value)
            except Exception as ex:
                print unicode(ex), sheet.cell(row, 33).value
            model.save()
    else:
        print "%sが見つかりません。" % path
