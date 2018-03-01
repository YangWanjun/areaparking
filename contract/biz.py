import datetime

from . import models
from utils import constants
from utils.errors import CustomException
from utils.mail import EbMail


def send_mail_from_view(task, request, mail_data):
    mail = EbMail(**mail_data)
    mail.send_email(user=request.user)
    task.status = '99'  # タスク完了
    task.updated_user = request.user
    task.save()
    json = {
        'status': '99',
        'updated_date': datetime.datetime.now(),
        'updated_user_name': '%s %s' % (request.user.last_name, request.user.first_name),
    }
    return json


def subscription_to_contract(subscription):
    """申込から成約になる

    :param subscription:
    :return:
    """
    if subscription.process and not subscription.process.is_finished:
        # プロセスの完了チェック
        raise CustomException(constants.ERROR_SUBSCRIPTION_PROCESS_NOT_FINISHED)
    if not subscription.car_maker or not subscription.car_model:
        # 契約車両必須
        raise CustomException(constants.ERROR_SUBSCRIPTION_NO_CAR)
    # 申込者情報を契約者情報に変更する
    contractor = models.Contractor()
    # contractor.code = subscription.code
    contractor.category = subscription.category
    contractor.name = subscription.name
    contractor.kana = subscription.kana
    contractor.post_code = subscription.get_post_code()
    contractor.address1 = subscription.address1
    contractor.address2 = subscription.address2
    contractor.tel = subscription.tel
    contractor.fax = subscription.fax
    contractor.email = subscription.email
    contractor.comment = subscription.comment
    contractor.personal_phone = subscription.personal_phone
    contractor.personal_gender = subscription.personal_gender
    contractor.personal_birthday = subscription.personal_birthday
    contractor.corporate_business_type = subscription.corporate_business_type
    contractor.corporate_web_site = subscription.corporate_web_site
    contractor.corporate_president = subscription.corporate_president
    contractor.corporate_staff_name = subscription.corporate_staff_name
    contractor.corporate_staff_kana = subscription.corporate_staff_kana
    contractor.corporate_staff_email = subscription.corporate_staff_email
    contractor.corporate_staff_tel = subscription.corporate_staff_tel
    contractor.corporate_staff_fax = subscription.corporate_staff_fax
    contractor.corporate_staff_phone = subscription.corporate_staff_phone
    contractor.corporate_staff_department = subscription.corporate_staff_department
    contractor.corporate_staff_position = subscription.corporate_staff_position
    contractor.corporate_capital = subscription.corporate_capital
    contractor.corporate_turnover = subscription.corporate_turnover
    contractor.corporate_user_name = subscription.corporate_user_name
    contractor.corporate_user_kana = subscription.corporate_user_kana
    contractor.corporate_user_tel = subscription.corporate_user_tel
    contractor.corporate_user_post_code = subscription.get_corporate_user_post_code()
    contractor.corporate_user_address1 = subscription.corporate_user_address1
    contractor.workplace_name = subscription.workplace_name
    contractor.workplace_post_code = subscription.get_workplace_post_code()
    contractor.workplace_address1 = subscription.workplace_address1
    contractor.workplace_address2 = subscription.workplace_address2
    contractor.workplace_tel = subscription.workplace_tel
    contractor.workplace_fax = subscription.workplace_fax
    contractor.workplace_comment = subscription.workplace_comment
    contractor.contact_name = subscription.contact_name
    contractor.contact_kana = subscription.contact_kana
    contractor.contact_address1 = subscription.contact_address1
    contractor.contact_address2 = subscription.contact_address2
    contractor.contact_tel = subscription.contact_tel
    contractor.contact_fax = subscription.contact_fax
    contractor.contact_relation = subscription.contact_relation
    contractor.delivery_type = subscription.delivery_type
    contractor.delivery_honorific = subscription.delivery_honorific
    contractor.delivery_name = subscription.delivery_name
    contractor.delivery_kana = subscription.delivery_kana
    contractor.delivery_post_code = subscription.delivery_post_code
    contractor.delivery_address1 = subscription.delivery_address1
    contractor.delivery_address2 = subscription.delivery_address2
    contractor.delivery_tel = subscription.delivery_tel
    contractor.delivery_fax = subscription.delivery_fax
    contractor.guarantor_name = subscription.guarantor_name
    contractor.guarantor_kana = subscription.guarantor_kana
    contractor.guarantor_birthday = subscription.guarantor_birthday
    contractor.guarantor_post_code = subscription.guarantor_post_code
    contractor.guarantor_address1 = subscription.guarantor_address1
    contractor.guarantor_address2 = subscription.guarantor_address2
    contractor.guarantor_tel = subscription.guarantor_tel
    contractor.guarantor_fax = subscription.guarantor_fax
    contractor.guarantor_relation = subscription.guarantor_relation
    contractor.guarantor_comment = subscription.guarantor_comment
    contractor.status = '11'        # 本契約
    contractor.save()
    # 車情報を保存する
    car = models.ContractorCar()
    car.contractor = contractor
    car.car_maker = subscription.car_maker
    car.car_model = subscription.car_model
    car.car_color = subscription.car_color
    car.car_no_plate = subscription.car_no_plate
    car.car_length = subscription.car_length
    car.car_width = subscription.car_width
    car.car_height = subscription.car_height
    car.car_weight = subscription.car_weight
    car.car_min_height = subscription.car_min_height
    car.car_f_value = subscription.car_f_value
    car.car_r_value = subscription.car_r_value
    car.car_comment = subscription.car_comment
    car.insurance_join_status = subscription.insurance_join_status
    car.insurance_limit_amount = subscription.insurance_limit_amount
    car.insurance_expire_date = subscription.insurance_expire_date
    car.save()
    # 契約情報
    contract = models.Contract(
        parking_lot=subscription.parking_lot,
        parking_position=subscription.parking_position,
        contractor=contractor,
        subscription=subscription,
        contract_date=datetime.date.today(),
        start_date=subscription.contract_start_date,
        end_date=subscription.get_contract_end_date(),
        notify_start_date=subscription.get_notify_start_date(),
        notify_end_date=subscription.get_notify_end_date(),
        staff=subscription.parking_lot.staff,
        car=car,
        status='11',
    )
    contract.save()
    # 入金項目
    for payment in subscription.contractpayment_set.all():
        payment.contract = contract
        payment.save()
    return contract


def get_year_list():
    start_year = 2010
    end_year = datetime.date.today().year + 1
    return range(start_year, end_year)
