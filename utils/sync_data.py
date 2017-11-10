# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import os
import xlrd
import datetime

import common

from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone

from master.models import CarModel, CarMaker
from parkinglot.models import ParkingLot
from revolution.models import MBrui, BkMst, HyMst, MTanto

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


def sync_buken_master(path):
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
                    room = HyMst.objects.get(bk_no=buken.bk_no, hy_no=row)
                except ObjectDoesNotExist:
                    room = HyMst()
                    room.bk_no = buken.bk_no
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


def sync_buken_tanto(path):
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


def sync_parking_lot(path):
    if os.path.exists(path):
        book = xlrd.open_workbook(path)
        sheet = book.sheet_by_index(0)
        for row in range(sheet.nrows):
            if row == 0:
                continue
            bk_no = sheet.cell(row, 10).value
            if isinstance(bk_no, basestring) and bk_no.find('/') > 0:
                bk_no = bk_no.split('/')[1]
            if not bk_no:
                continue
            try:
                bk_no = int(bk_no)
            except:
                continue
            try:
                parking_lot = ParkingLot.objects.get(buken=bk_no)
                parking_lot.is_existed_contractor_allowed = sheet.cell(row, 18).value == "○"
                parking_lot.is_new_contractor_allowed = sheet.cell(row, 19).value == "○"
                excel_date = sheet.cell(row, 20).value
                if isinstance(excel_date, (int, float)):
                    excel_date = int(excel_date)
                    parking_lot.free_end_date = datetime.datetime.fromordinal(datetime.datetime(1900, 1, 1).toordinal() + excel_date - 2).date()
                parking_lot.save()
            except ObjectDoesNotExist:
                print bk_no, 'not existed'


def sync_parking_size(path):
    if os.path.exists(path):
        book = xlrd.open_workbook(path)
        sheet = book.sheet_by_index(1)
        current_name = None
        for row in range(sheet.nrows):
            if row < 4:
                continue
            address = sheet.cell(row, 2).value
            name = sheet.cell(row, 3).value
            if name and address and current_name != name:
                current_name = name.rstrip("駐車場")
                queryset = ParkingLot.objects.public_filter(buken__bk_name__icontains=current_name)
                if queryset.count() == 0:
                    print '{}行目'.format(row + 1), current_name, 'not exists'
                elif queryset.count() > 1:
                    print '{}行目'.format(row + 1), current_name, 'multi existed'
                else:
                    parking_lot = queryset.first()
                    i = 0
                    position_list = []
                    while (not sheet.cell(row + i, 2).value or not sheet.cell(row + i, 3).value or i == 0) and (row + i) < sheet.nrows:
                        length = sheet.cell(row, 4).value
                        width = sheet.cell(row, 5).value
                        height = sheet.cell(row, 6).value
                        weight = sheet.cell(row, 7).value
                        tyre_width = sheet.cell(row, 8).value
                        tyre_width_ap = sheet.cell(row, 9).value
                        min_height = sheet.cell(row, 10).value
                        min_height_ap = sheet.cell(row, 11).value
                        f_value = sheet.cell(row, 12).value
                        r_value = sheet.cell(row, 13).value
                        comment = sheet.cell(row, 23).value
                        position_list.append({
                            'length': length if isinstance(length, (int, float)) else None,
                            'width': width if isinstance(width, (int, float)) else None,
                            'height': height if isinstance(height, (int, float)) else None,
                            'weight': weight if isinstance(weight, (int, float)) else None,
                            'tyre_width': tyre_width if isinstance(tyre_width, (int, float)) else None,
                            'tyre_width_ap': tyre_width_ap if isinstance(tyre_width_ap, (int, float)) else None,
                            'min_height': min_height if isinstance(min_height, (int, float)) else None,
                            'min_height_ap': min_height_ap if isinstance(min_height_ap, (int, float)) else None,
                            'f_value': f_value if isinstance(f_value, (int, float)) else None,
                            'r_value': r_value if isinstance(r_value, (int, float)) else None,
                            'comment': comment,
                        })
                        i += 1
                    for i, parking_position in enumerate(parking_lot.parkingposition_set.all()):
                        if i >= len(position_list):
                            break
                        parking_position.length = position_list[i].get('length', None)
                        parking_position.width = position_list[i].get('width', None)
                        parking_position.height = position_list[i].get('height', None)
                        parking_position.weight = position_list[i].get('weight', None)
                        parking_position.tyre_width = position_list[i].get('tyre_width', None)
                        parking_position.tyre_width_ap = position_list[i].get('tyre_width_ap', None)
                        parking_position.min_height = position_list[i].get('min_height', None)
                        parking_position.min_height_ap = position_list[i].get('min_height_ap', None)
                        parking_position.f_value = position_list[i].get('f_value', None)
                        parking_position.r_value = position_list[i].get('r_value', None)
                        parking_position.comment = position_list[i].get('comment', None)
                        parking_position.save()

            elif name and not address:
                print '{}行目'.format(row + 1), '駐車場名', name, 'skipped'
            elif not name and address:
                print '{}行目'.format(row + 1), '住所', address, 'skipped'
