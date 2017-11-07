# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import os
import xlrd
import datetime
import re

import common

from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Value as V, CharField
from django.db.models.functions import Concat
from django.utils import timezone

from master.models import CarModel, CarMaker, ParkingLotType
from parkinglot.models import ParkingLot, ParkingPosition, ParkingLotStaff
from department.models import Member
from revolution.models import MBrui, BkMst, BaiRooms, MTanto

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


def sync_buken_master():
    path = b"C:\Users\EB097\Documents\whiteboard.xlsx"
    if os.path.exists(path):
        book = xlrd.open_workbook(path)
        sheet = book.sheet_by_index(0)
        for row in range(sheet.nrows):
            if row == 0:
                continue
            bk_no = 0
            try:
                bk_no = sheet.cell(row, 10).value
                if isinstance(bk_no, basestring) and bk_no.find('/') > 0:
                    bk_no = bk_no.split('/')[1]
                if not bk_no:
                    continue
                bk_no = int(bk_no)
                # 駐車場分類
                brui_name = sheet.cell(row, 26).value
                if not brui_name:
                    brui_name = "その他"
                try:
                    brui = MBrui.objects.get(brui_name=brui_name)
                except ObjectDoesNotExist:
                    brui = MBrui()
                    brui.brui_no = row
                    brui.brui_name = brui_name
                    brui.kosin_date = timezone.now()
                    brui.save()
                # 駐車場
                try:
                    buken = BkMst.objects.get(bk_no=bk_no)
                except ObjectDoesNotExist:
                    buken = BkMst()
                    buken.bk_no = bk_no
                    buken.bk_name = sheet.cell(row, 25).value
                    buken.brui = brui
                    buken.ken_no = 13
                    buken.add_ken = "東京都"
                    buken.si_no = '13110'
                    buken.add_si = sheet.cell(row, 9).value + "区"
                    locations = sheet.cell(row, 22).value.split('/')
                    if len(locations) == 2:
                        buken.add_cyo = locations[1]
                        buken.kotsu1 = locations[0]
                    else:
                        buken.add_cyo = sheet.cell(row, 22).value
                    # buken.is_existed_contractor_allowed = sheet.cell(row, 18).value == "○"
                    # buken.is_new_contractor_allowed = sheet.cell(row, 19).value == "○"
                    free_end_date = sheet.cell(row, 20).value
                    if isinstance(free_end_date, datetime.date):
                        # buken.free_end_date = free_end_date
                        pass
                    buken.save()
                # 車室
                try:
                    room = BaiRooms.objects.get(buken=buken, naibu_no=row)
                except ObjectDoesNotExist:
                    room = BaiRooms()
                    room.buken = buken
                    room.naibu_no = row
                    room.hy_no = 'No.{}'.format(row)
                    room.kosin_date = timezone.now()
                    # room.price_recruitment = sheet.cell(row, 28).value or None
                    # room.price_recruitment_no_tax = sheet.cell(row, 29).value or None
                    # room.price_homepage = sheet.cell(row, 32).value or None
                    # room.price_homepage_no_tax = sheet.cell(row, 31).value or None
                    # room.price_handbill = sheet.cell(row, 34).value or None
                    # room.price_handbill_no_tax = sheet.cell(row, 33).value or None
                    room.save()
            except Exception as ex:
                print row, bk_no, unicode(ex)


def sync_buken_tanto():
    path = b"C:\Users\EB097\Documents\whiteboard.xlsx"
    if os.path.exists(path):
        book = xlrd.open_workbook(path)
        sheet = book.sheet_by_index(0)
        for row in range(sheet.nrows):
            if row == 0:
                continue
            bk_no = sheet.cell(row, 44).value
            name = sheet.cell(row, 50).value
            if bk_no and name:
                try:
                    buken = BkMst.objects.get(pk=bk_no)
                    try:
                        member = MTanto.objects.get(tanto_name=name)
                    except ObjectDoesNotExist:
                        member = MTanto(tanto_no=row, tanto_name=name)
                        member.save()
                    if not buken.tanto:
                        buken.tanto = member
                        buken.save()
                    else:
                        print name, 'existed'
                except ObjectDoesNotExist:
                    print bk_no, 'not existed'
