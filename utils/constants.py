# -*- coding: utf-8 -*-
from __future__ import unicode_literals


SYSTEM_NAME = "エリアパーキング"
END_DATE = '9999-12-31'

DATABASE_DEFAULT = "default"
DATABASE_REVOLUTION = "fk5dtsql"

CONFIG_GROUP_SYSTEM = 'system'
CONFIG_EMAIL_ADDRESS = 'email_address'
CONFIG_EMAIL_SMTP_HOST = 'email_smtp_host'
CONFIG_EMAIL_SMTP_PORT = 'email_smtp_port'
CONFIG_EMAIL_PASSWORD = 'email_password'
CONFIG_CIRCLE_RADIUS = 'circle_radius'

REG_TEL = r'^\d+\[0-9-]+d+$'
REG_POST_CODE = r"\d{3}[-]?\d{4}"

CHOICE_CONTRACTOR_TYPE = (
    ('1', '個人'),
    ('2', '法人'),
)
CHOICE_GENDER = (
    ('1', '男'),
    ('2', '女'),
)
CHOICE_MARRIED = (
    ('0', "未婚"),
    ('1', "既婚"),
)
CHOICE_PAPER_DELIVERY_TYPE = (
    ('01', '基本情報の住所'),
    ('02', '勤務先'),
    ('03', '連絡先'),
    ('04', '保証人'),
    ('99', 'その他'),
)
CHOICE_HONORIFIC = (
    ('1', '様'),
    ('2', '御中'),
)
CHOICE_BANK_ACCOUNT_TYPE = (
    (1, "普通預金"),
    (2, "定期預金"),
    (3, "総合口座"),
    (4, "当座預金"),
    (5, "貯蓄預金"),
    (6, "大口定期預金"),
    (7, "積立定期預金")
)
CHOICE_BANK_POST_KBN = (
    (1, "銀行"),
    (2, "郵便局"),
)
CHOICE_MANAGEMENT_TYPE = (
    ('01', '管理委託'),
    ('02', '一括借上'),
    ('03', '一般物件'),
    ('04', '自社物件'),
)
CHOICE_KEY_CATEGORY = (
    ('01', '鍵'),
    ('02', 'カード'),
    ('03', 'リモコン'),
    ('04', 'その他の鍵'),
)
CHOICE_PAY_TIMING = (
    ('01', '契約時'),
    ('02', '更新時'),
    ('03', '毎月'),
)
CHOICE_CONTRACT_STATUS = (
    ('01', '空き'),
    ('02', '手続中'),
    ('03', '空きなし'),
)
CHOICE_MAIL_GROUP = (
    ('001', '申込書送付'),
    ('011', '契約書送付'),
)
CHOICE_REPORT_KBN = (
    ('01', '申込書'),
    ('02', '申込確認書'),
    # ('01', '申込書'),
    # ('01', '申込書'),
    # ('01', '申込書'),
    # ('01', '申込書'),
    # ('01', '申込書'),
    # ('01', '申込書'),
    # ('01', '申込書'),
    # ('01', '申込書'),
)
CHOICE_CONTRACT_PROCESS = (
    ('01', '申込み'),
    ('02', '住所・電話番号 審査・確認'),
    ('01', '勤め先審査'),
    ('01', '申込み'),
    ('01', '申込み'),
    ('01', '申込み'),
    ('01', '申込み'),
)
