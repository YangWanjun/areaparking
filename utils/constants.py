# -*- coding: utf-8 -*-
from __future__ import unicode_literals


SYSTEM_NAME = "エリアパーキング"
END_DATE = '9999-12-31'

DATABASE_DEFAULT = "default"
DATABASE_REVOLUTION = "fk5dtsql"

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
