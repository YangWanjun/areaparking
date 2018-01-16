# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import os
import re
import xlrd
import datetime
import requests

from django.core.exceptions import ObjectDoesNotExist

from . import common
from master.models import CarModel, CarMaker, Config, Company, Payment, MailTemplate, MailGroup, TransmissionRoute
from parkinglot.models import ParkingLot, ParkingLotType, ParkingPosition, ParkingLotStaffHistory
from employee.models import Department, Member, MemberShip


def sync_master():
    # 自社情報の同期
    if Company.objects.public_all().count() == 0:
        company = Company()
        company.name = "株式会社○○○・○○○○○"
        company.post_code = '123-4567'
        company.address1 = '東京都港区芝2丁目'
        company.address2 = '２－２－２○○ビル　１０階'
        company.tel = '080-1234-5678'
        company.fax = '070-1234-5678'
        company.email = 'email@example.com'
        company.save()
        print('作成', '自社情報は作成しました。')
    # 入金項目
    if Payment.objects.public_filter(timing='10').count() == 0:
        Payment.objects.create(timing='10', name="契約時事務手数料", amount=10000)
        print('作成', '契約時事務手数料は作成しました。')
    if Payment.objects.public_filter(timing='11').count() == 0:
        Payment.objects.create(timing='11', name="契約開始月末日までの日割賃料")
        print('作成', '契約時事務手数料は作成しました')
    if Payment.objects.public_filter(timing='30').count() == 0:
        Payment.objects.create(timing='30', name="翌月分の賃料")
        print('作成', '契約時事務手数料は作成しました')
    if Payment.objects.public_filter(timing='41').count() == 0:
        Payment.objects.create(timing='41', name="保管場所承諾証明書発行手数料", amount=10000)
        print('作成', '保管場所承諾証明書発行手数料は作成しました')
    # 申込書送付のメールテンプレート
    if MailGroup.objects.public_filter(code='001').count() == 0:
        template = MailTemplate.objects.create(title='申込書送付', body="""<!DOCTYPE html>
<html>
<head>
</head>
<body>
<p>{{ user_name }} 様：&nbsp;</p>
<p>いつもお世話になっております、<br />株式会社エリアパーキングです。</p>
<p>このたび駐車場のご申込みいただき<br />誠にありがとうございます。</p>
<p>下記のURLにて、お申込みください。</p>
<p>■申込書<br /><a title="申込書" href="{{user_subscription_url}}" data-mce-href="{{user_subscription_url}}" target="_blank" rel="noopener">{{user_subscription_url}}</a></p>
</body>
</html>""")
        MailGroup.objects.create(code='001', name="申込書送付", sender='ap.test@e-business.co.jp', template=template)
        print('作成', '申込書送付のメールグループ')
    if MailGroup.objects.public_filter(code='002').count() == 0:
        template = MailTemplate.objects.create(title='ご申込ありがとうございます！', body="""<!DOCTYPE html>
<html>
<head>
</head>
<body>
<p>{{ user_name }} {{user_honorific}}：&nbsp;</p>
<p>いつもお世話になっております、<br />株式会社エリアパーキングです。</p>
<p>このたび駐車場のご申込みいただき<br />誠にありがとうございます。</p>
<p>お客様のご申込を下記内容にて承りましたので、どうぞご確認くださいませ。<br />=======================================================================</p>
<p>{{subscription_result}}</p>
</body>
</html>""")
        MailGroup.objects.create(code='002', name="申込完了", sender='ap.test@e-business.co.jp', template=template)
        print('作成', '申込完了のメールグループ')
    if MailGroup.objects.public_filter(code='011').count() == 0:
        template = MailTemplate.objects.create(title='契約書類送付', body="""<!DOCTYPE html>
<html>
<head>
</head>
<body>
<p>{{ user_name }} 様：&nbsp;</p>
<p>いつもお世話になっております、<br />株式会社エリアパーキングです。</p>
<p>平素は格別のご高配を賜り、厚く御礼申し上げます。<br />下記のとおりご契約書類を送付致しますのでよろしくお願い致します。</p>
<p>下記のURLにて、ご確認ください。</p>
<p>■契約書類<br /><a title="契約書類" href="{{user_contract_url}}" target="_blank" rel="noopener">{{user_contract_url}}</a></p>
</body>
</html>""")
        MailGroup.objects.create(code='011', name="契約書類送付", sender='ap.test@e-business.co.jp', template=template)
        print('作成', '契約書類送付のメールグループ')
    if MailGroup.objects.public_filter(code='012').count() == 0:
        template = MailTemplate.objects.create(title='ご契約ありがとうございます！', body="""<!DOCTYPE html>
<html>
<head>
</head>
<body>
<p>{{ user_name }} {{user_honorific}}：&nbsp;</p>
<p>いつもお世話になっております、<br />株式会社エリアパーキングです。</p>
<p>ご契約は完了しましたので、お知らせいたします。</p>
</body>
</html>""")
        MailGroup.objects.create(code='012', name="契約完了", sender='ap.test@e-business.co.jp', template=template)
        print('作成', '契約完了のメールグループ')
    if MailGroup.objects.public_filter(code='310').count() == 0:
        template = MailTemplate.objects.create(title='{{parking_lot_name}}の退出届', body="""<!DOCTYPE html>
<html>
<head>
</head>
<body>
<p>{{ user_name }} {{user_honorific}}：&nbsp;</p>
<p>いつもお世話になっております、<br />株式会社エリアパーキングです。</p>
<p>ご解約は下記のＵＲＬにて進んでください。</p>
<p>■解約手続き<br/><a title="解約書類" href="{{user_cancellation_url}}" target="_blank" rel="noopener">{{user_cancellation_url}}</a></p>
</body>
</html>""")
        MailGroup.objects.create(code='310', name="一般解約書類送付", sender='ap.test@e-business.co.jp', template=template)
        print('作成', '一般解約書類送付のメールグループ')
    # 媒体を作成
    if TransmissionRoute.objects.public_all().count() == 0:
        TransmissionRoute.objects.create(name='チラシ', price_kbn='01')
        TransmissionRoute.objects.create(name='インターネット', price_kbn='02')
        TransmissionRoute.objects.create(name='看板',)
        TransmissionRoute.objects.create(name='新聞折込',)
        TransmissionRoute.objects.create(name='不動産紹介',)
        TransmissionRoute.objects.create(name='知人紹介',)
        TransmissionRoute.objects.create(name='その他',)
        print('作成', '媒体一覧')


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
            except Exception as ex:
                print(maker_name, "保存失敗", ex)
            try:
                model = CarModel.objects.get(maker=maker, name=name, grade_name=grade_name)
            except Exception:
                model = CarModel(maker=maker, name=name, grade_name=grade_name)
            try:
                model.sale_date = datetime.datetime.strptime(sheet.cell(row, 7).value.encode('utf8'), "%Y年%m月%d日".encode('utf8'))
            except Exception as ex:
                print(ex, sheet.cell(row, 7).value)
            try:
                    model.length = common.get_num_from_str(sheet.cell(row, 29).value)
            except Exception as ex:
                print(ex, sheet.cell(row,29).value)
            try:
                model.width = common.get_num_from_str(sheet.cell(row, 30).value)
            except Exception as ex:
                print(ex, sheet.cell(row, 30).value)
            try:
                model.height = common.get_num_from_str(sheet.cell(row, 31).value)
            except Exception as ex:
                print(ex, sheet.cell(row, 31).value)
            try:
                model.weight = common.get_num_from_str(sheet.cell(row, 17).value)
            except Exception as ex:
                print(ex, sheet.cell(row, 17).value)
            try:
                model.min_height = common.get_num_from_str(sheet.cell(row, 33).value)
            except Exception as ex:
                print(ex, sheet.cell(row, 33).value)
            try:
                model.save()
            except Exception as ex:
                print(maker_name, "モデル保存失敗", ex)
    else:
        print("%sが見つかりません。" % path)


def sync_employee(path):
    if os.path.exists(path):
        book = xlrd.open_workbook(path)
        sheet = book.sheet_by_index(0)
        start_date = datetime.date(2010, 1, 1)
        try:
            department = Department.objects.get(name="リーシング")
        except ObjectDoesNotExist:
            department = Department(name="リーシング")
            department.save()

        for row in range(sheet.nrows):
            if row < 3:
                continue
            name = sheet.cell(row, 50).value
            if not name:
                continue

            parts = re.split(r'\s+', name)
            if len(parts) > 1:
                first_name = parts[0]
                last_name = parts[1]
            else:
                first_name = name
                last_name = "様"
            try:
                Member.objects.get(first_name=first_name, last_name=last_name)
            except ObjectDoesNotExist:
                member = Member(first_name=first_name, last_name=last_name)
                member.save()
                MemberShip.objects.create(member=member, department=department, start_date=start_date, end_date='9999-12-31')


def sync_parking_lot(path):
    if os.path.exists(path):
        book = xlrd.open_workbook(path)
        sheet = book.sheet_by_index(0)
        for row in range(sheet.nrows):
            if row == 0:
                continue
            bk_no = 0
            try:
                bk_no = sheet.cell(row, 10).value
                if isinstance(bk_no, str) and bk_no.find('/') > 0:
                    bk_no = bk_no.split('/')[1]
                if not bk_no:
                    continue
                if isinstance(bk_no, str) and not re.match(r'^\d+$', bk_no):
                    continue
                bk_no = int(bk_no)
                # 駐車場分類
                category = sheet.cell(row, 26).value
                if not category:
                    category = "その他"
                try:
                    lot_type = ParkingLotType.objects.get(name=category)
                except ObjectDoesNotExist:
                    lot_type = ParkingLotType()
                    lot_type.code = row
                    lot_type.name = category
                    lot_type.save()
                # 駐車場
                try:
                    lot = ParkingLot.objects.get(code=bk_no)
                except ObjectDoesNotExist:
                    lot = ParkingLot()
                    lot.code = bk_no
                    lot.name = sheet.cell(row, 25).value
                    lot.category = lot_type
                    lot.pref_code = 13
                    lot.pref_name = "東京都"
                    lot.city_code = '13110'
                    lot.city_name = sheet.cell(row, 9).value + "区"
                    locations = sheet.cell(row, 22).value.split('/')
                    if len(locations) == 2:
                        lot.town_name = locations[1]
                        lot.traffic = locations[0]
                    else:
                        lot.town_name = sheet.cell(row, 22).value
                    lot.is_existed_contractor_allowed = sheet.cell(row, 18).value == "○"
                    lot.is_new_contractor_allowed = sheet.cell(row, 19).value == "○"
                    free_end_date = sheet.cell(row, 20).value
                    if isinstance(free_end_date, datetime.date):
                        lot.free_end_date = free_end_date
                    lot.save()
                # 車室
                room_name = 'No.{}'.format(row)
                try:
                    room = ParkingPosition.objects.get(parking_lot=lot, name=room_name)
                except ObjectDoesNotExist:
                    room = ParkingPosition()
                    room.parking_lot = lot
                    room.name = room_name
                    if sheet.cell(row, 28).value and isinstance(sheet.cell(row, 28).value, (int, float)):
                        room.price_recruitment = sheet.cell(row, 28).value or None
                    if sheet.cell(row, 29).value and isinstance(sheet.cell(row, 29).value, (int, float)):
                        room.price_recruitment_no_tax = sheet.cell(row, 29).value or None
                    if sheet.cell(row, 32).value and isinstance(sheet.cell(row, 32).value, (int, float)):
                        room.price_homepage = sheet.cell(row, 32).value or None
                    if sheet.cell(row, 31).value and isinstance(sheet.cell(row, 31).value, (int, float)):
                        room.price_homepage_no_tax = sheet.cell(row, 31).value or None
                    if sheet.cell(row, 34).value and isinstance(sheet.cell(row, 34).value, (int, float)):
                        room.price_handbill = sheet.cell(row, 34).value
                    if sheet.cell(row, 33).value and isinstance(sheet.cell(row, 33).value, (int, float)):
                        room.price_handbill_no_tax = sheet.cell(row, 33).value
                    room.save()
            except Exception as ex:
                print(row, bk_no, ex)
                raise ex


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
                queryset = ParkingLot.objects.public_filter(name__icontains=current_name)
                if queryset.count() == 0:
                    print('{}行目'.format(row + 1), current_name, 'not exists')
                elif queryset.count() > 1:
                    print('{}行目'.format(row + 1), current_name, 'multi existed')
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
                print('{}行目'.format(row + 1), '駐車場名', name, 'skipped')
            elif not name and address:
                print('{}行目'.format(row + 1), '住所', address, 'skipped')


def sync_parking_lot_staff(path):
    if os.path.exists(path):
        book = xlrd.open_workbook(path)
        sheet = book.sheet_by_index(0)
        for row in range(sheet.nrows):
            if row < 3:
                continue
            bk_no = sheet.cell(row, 44).value
            name = sheet.cell(row, 50).value
            parts = re.split(r'\s+', name)
            if len(parts) > 1:
                first_name = parts[0]
                last_name = parts[1]
            else:
                first_name = name
                last_name = "様"
            if bk_no and isinstance(bk_no, (int, float)):
                try:
                    parking_lot = ParkingLot.objects.get(code=bk_no)
                except ObjectDoesNotExist:
                    continue
                try:
                    member = Member.objects.get(first_name=first_name, last_name=last_name)
                except ObjectDoesNotExist:
                    continue
                parking_lot.staff = member
                parking_lot.staff_start_date = datetime.date(2017, 1, 1)
                parking_lot.save()


# def sync_waiting_list(path):
#     if os.path.exists(path):
#         book = xlrd.open_workbook(path)
#         sheet = book.sheet_by_name("順番待ﾘｽﾄ")
#         for row in range(sheet.nrows):
#             if row < 2:
#                 continue
#             waiting = Waiting()
#             excel_date = sheet.cell(row, 0).value
#             if isinstance(excel_date, (int, float)):
#                 excel_date = int(excel_date)
#                 waiting.created_date = waiting.updated_date = datetime.datetime.fromordinal(datetime.datetime(1900, 1, 1).toordinal() + excel_date - 2).date()
#             tanto_name = sheet.cell(row, 1).value
#             if tanto_name:
#                 pass
#                 # try:
#                 #     tanto = MTanto.objects.get(tanto_name__icontains=tanto_name)
#                 #     waiting.tanto_no = tanto.pk
#                 # except (ObjectDoesNotExist, MultipleObjectsReturned):
#                 #     pass
#             parking_lot_name = sheet.cell(row, 4).value
#             if parking_lot_name:
#                 try:
#                     waiting.parking_lot = ParkingLot.objects.get(buken__bk_name__icontains=parking_lot_name)
#                 except (ObjectDoesNotExist, MultipleObjectsReturned):
#                     continue
#
#             waiting.name = sheet.cell(row, 6).value or '氏名%s' % row
#             waiting.tel1 = sheet.cell(row, 8).value or '080-1234-4578'
#             waiting.tel2 = sheet.cell(row, 9).value or '070-1234-4578'
#             if sheet.cell(row, 13).value:
#                 cars = sheet.cell(row, 13).value.split("　")
#                 if cars == 2:
#                     waiting.car_maker = cars[0]
#                     waiting.car_model = cars[1]
#             waiting.length = sheet.cell(row, 14).value or None
#             waiting.width = sheet.cell(row, 15).value or None
#             waiting.height = sheet.cell(row, 16).value or None
#             waiting.weight = sheet.cell(row, 17).value or None
#             media = None
#             if sheet.cell(row, 18).value:
#                 media_name = sheet.cell(row, 18).value
#                 try:
#                     media = TransmissionRoute.objects.get(name=media_name)
#                 except ObjectDoesNotExist:
#                     media = TransmissionRoute(name=media_name)
#                     media.save()
#             waiting.media = media
#             waiting.price_handbill = sheet.cell(row, 19).value
#             waiting.comment = sheet.cell(row, 20).value
#             try:
#                 waiting.save()
#             except Exception as ex:
#                 print("%s行目" % row, ex)


def sync_coordinate(url):
    if not url:
        print("座標取得のＡＰＩを設定してください。")
        return
    queryset = ParkingLot.objects.public_filter(lng__isnull=True, lat__isnull=True)
    for parking_lot in queryset:
        address = parking_lot.address()
        if not address:
            continue

        r = requests.get(url, {'address': address})
        if r.status_code == 200:
            coordinate = r.json()
            parking_lot.lng = coordinate.get('lng', None)
            parking_lot.lat = coordinate.get('lat', None)
            parking_lot.save()
        else:
            print("エラー：", r.content)


def sync_config():
    configs = [
        ('email', 'email_address', 'ebprint@e-business.co.jp', None),
        ('email', 'email_password', '******', None),
        ('email', 'email_smtp_host', 'smtp.e-business.co.jp', None),
        ('email', 'email_smtp_port', '587', None),
        ('system', 'circle_radius', '2000', None),
        ('system', 'domain_name', 'http://ap.mopa.jp', None),
        ('system', 'page_size', '25', None),
        ('system', 'url_timeout', '24', "ＵＲＬのタイムアウト時間（単位：時間）"),
    ]
    for group, name, value, comment in configs:
        if Config.objects.public_filter(name=name).count() == 0:
            Config.objects.create(group=group, name=name, value=value, comment=comment)
