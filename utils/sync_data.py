# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import os
import xlrd
import datetime

import common

from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Value as V, CharField
from django.db.models.functions import Concat

from master.models import CarModel, CarMaker, ParkingLotType
from parkinglot.models import ParkingLot, ParkingPosition, ParkingLotStaff
from department.models import Member

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


def sync_whiteboard_area():
    path = b"C:\Users\EB097\Documents\whiteboard.xlsx"
    if os.path.exists(path):
        book = xlrd.open_workbook(path)
        sheet = book.sheet_by_index(0)
        for row in range(sheet.nrows):
            if row == 0:
                continue
            try:
                lot_no = sheet.cell(row, 10).value
                if isinstance(lot_no, basestring) and lot_no.find('/') > 0:
                    lot_no = lot_no.split('/')[1]
                # 駐車場分類
                lot_type = sheet.cell(row, 26).value
                if not lot_type:
                    lot_type = "その他"
                try:
                    parking_lot_type = ParkingLotType.objects.get(name=lot_type)
                except ObjectDoesNotExist:
                    parking_lot_type = ParkingLotType()
                    parking_lot_type.code = row
                    parking_lot_type.name = lot_type
                    parking_lot_type.save()
                # 駐車場
                try:
                    parking_lot = ParkingLot.objects.get(code=lot_no)
                except ObjectDoesNotExist:
                    parking_lot = ParkingLot()
                    parking_lot.code = lot_no
                    parking_lot.name = sheet.cell(row, 25).value
                    parking_lot.segment = parking_lot_type
                    parking_lot.pref_code = '13'
                    parking_lot.pref_name = "東京都"
                    parking_lot.city_code = '13110'
                    parking_lot.city_name = sheet.cell(row, 9).value + "区"
                    locations = sheet.cell(row, 22).value.split('/')
                    if len(locations) == 2:
                        parking_lot.town_name = locations[1]
                        parking_lot.nearest_station = locations[0]
                    else:
                        parking_lot.town_name = sheet.cell(row, 22).value
                    parking_lot.is_existed_contractor_allowed = sheet.cell(row, 18).value == "○"
                    parking_lot.is_new_contractor_allowed = sheet.cell(row, 19).value == "○"
                    free_end_date = sheet.cell(row, 20).value
                    if isinstance(free_end_date, datetime.date):
                        parking_lot.free_end_date = free_end_date
                    parking_lot.save()
                parking_position = ParkingPosition()
                parking_position.parking_lot = parking_lot
                parking_position.name = 'No.{}'.format(row)
                parking_position.price_recruitment = sheet.cell(row, 28).value or None
                parking_position.price_recruitment_no_tax = sheet.cell(row, 29).value or None
                parking_position.price_homepage = sheet.cell(row, 32).value or None
                parking_position.price_homepage_no_tax = sheet.cell(row, 31).value or None
                parking_position.price_handbill = sheet.cell(row, 34).value or None
                parking_position.price_handbill_no_tax = sheet.cell(row, 33).value or None
                parking_position.save()
            except Exception as ex:
                print row, unicode(ex)


def sync_parking_lot_staff():
    path = b"C:\Users\EB097\Documents\whiteboard.xlsx"
    if os.path.exists(path):
        book = xlrd.open_workbook(path)
        sheet = book.sheet_by_index(0)
        for row in range(sheet.nrows):
            if row == 0:
                continue
            lot_no = sheet.cell(row, 44).value
            name = sheet.cell(row, 50).value
            if lot_no and name:
                try:
                    parking_lot = ParkingLot.objects.get(code=lot_no)
                    try:
                        member = Member.objects.annotate(
                            name=Concat('first_name', V('　'), 'last_name', output_field=CharField())
                        ).get(name=name)
                        if ParkingLotStaff.objects.public_filter(parking_lot=parking_lot, member=member).count() == 0:
                            print 'Adding', name
                            staff = ParkingLotStaff(parking_lot=parking_lot, member=member, start_date="2017-01-01")
                            staff.save()
                        else:
                            print name, 'existed'
                    except ObjectDoesNotExist:
                        print name, 'not existed'
                except ObjectDoesNotExist:
                    print lot_no, 'not existed'


if __name__ == '__main__':
    sync_whiteboard_area()
