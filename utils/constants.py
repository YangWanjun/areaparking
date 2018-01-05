# -*- coding: utf-8 -*-
from __future__ import unicode_literals


SYSTEM_NAME = "エリアパーキング"
END_DATE = '9999-12-31'

DATABASE_DEFAULT = "default"
DATABASE_REVOLUTION = "fk5dtsql"

MIME_TYPE_EXCEL = 'application/excel'
MIME_TYPE_PDF = 'application/pdf'
MIME_TYPE_ZIP = 'application/zip'
MIME_TYPE_HTML = 'text/html'

CONFIG_GROUP_SYSTEM = 'system'
CONFIG_GROUP_EMAIL = 'email'
CONFIG_GROUP_ADJUST_SIZE = 'size'
CONFIG_EMAIL_ADDRESS = 'email_address'
CONFIG_EMAIL_SMTP_HOST = 'email_smtp_host'
CONFIG_EMAIL_SMTP_PORT = 'email_smtp_port'
CONFIG_EMAIL_PASSWORD = 'email_password'
CONFIG_CIRCLE_RADIUS = 'circle_radius'
CONFIG_DOMAIN_NAME = 'domain_name'
CONFIG_PAGE_SIZE = 'page_size'
CONFIG_DECIMAL_TYPE = 'decimal_type'
CONFIG_CONSUMPTION_TAX_RATE = 'consumption_tax_rate'
CONFIG_CAR_LENGTH_ADJUST = 'car_length_adjust'
CONFIG_CAR_WIDTH_ADJUST = 'car_width_adjust'
CONFIG_CAR_HEIGHT_ADJUST = 'car_height_adjust'
CONFIG_CAR_WEIGHT_ADJUST = 'car_weight_adjust'
CONFIG_URL_TIMEOUT = 'url_timeout'
CONFIG_GCM_URL = 'gcm_url'
CONFIG_FIREBASE_SERVERKEY = 'firebase_serverkey'

REG_TEL = r'^\d+[0-9-]+\d+$'
REG_POST_CODE = r"\d{3}[-]?\d{4}"

REPORT_SUBSCRIPTION_CONFIRM = "申込確認書"
REPORT_SUBSCRIPTION = "申込書"

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
    ('10', '契約時'),
    ('11', '契約開始月'),
    ('20', '更新時'),
    ('30', '翌月以降'),
    ('40', '一時'),
    ('41', '保管場所承諾証明書発行手数料'),
)
CHOICE_TAX_KBN = (
    ('1', '税抜'),
    ('2', '税込'),
)
CHOICE_DECIMAL_TYPE = (
    ('0', '切り捨て'),
    ('1', '四捨五入'),
    ('2', '切り上げ'),
)
CHOICE_PRICE_KBN = (
    ('01', 'チラシ価格'),
    ('02', 'ホームページ価格'),
)
CHOICE_PARKING_STATUS = (
    ('01', '空き'),
    ('02', '手続中'),
    ('03', '空無'),
    ('04', '仮押さえ'),
)
CHOICE_MAIL_GROUP = (
    ('001', '申込書送付'),
    ('002', '申込完了'),
    ('011', '契約書送付'),
)
CHOICE_REPORT_KBN = (
    ('001', REPORT_SUBSCRIPTION),
    ('002', REPORT_SUBSCRIPTION_CONFIRM),
    # ('01', '申込書'),
    # ('01', '申込書'),
    # ('01', '申込書'),
    # ('01', '申込書'),
    # ('01', '申込書'),
    # ('01', '申込書'),
    # ('01', '申込書'),
    # ('01', '申込書'),
)
CHOICE_PROCESS = (
    ('01', '申込みから成約まで'),
)
CHOICE_TASK_CATEGORY = (
    # 01 申込
    ('010', '申込書送付'),
    ('011', '申込書確認'),
    # 03 審査
    ('030', '住所・電話番号 審査・確認'),
    ('031', '勤め先審査'),
    ('032', '車両サイズ審査'),
    ('033', '申込ルート元審査'),
    # 契約
    ('100', '契約書類一式の送付'),
    # 入金
    ('110', '入金確認'),
)
CHOICE_TASK_STATUS = (
    ('01', '未実施'),
    ('02', '実施中'),
    ('10', 'スキップ'),
    ('20', '見送る'),
    ('91', 'キャンセル'),
    ('99', '完了'),
)
CHOICE_CONTRACT_STATUS = (
    ('01', '仮契約'),
    ('11', '本契約'),
    ('21', '破棄'),
)
CHOICE_SUBSCRIPTION_STATUS = (
    ('01', '新規申込'),
    ('02', '申込完了'),
    ('03', '契約手続中'),
    ('11', '成約'),
    ('12', '破棄'),
)
CHOICE_INSURANCE_TYPE = (
    ('within', '制限あり'),
    ('without', '無制限'),
    ('plans', '加入予定'),
)
CHOICE_CONTRACT_PERIOD = (
    ('long', '１年間（その後自動更新）'),
    ('short', '１・２ヶ月契約'),
)
CHOICE_IS_REQUIRED = (
    ('yes', '必要'),
    ('no', '不要'),
)

ERROR_SETTING_NO_SUBSCRIPTION = "申込書の出力書式が設定されていません、管理サイトで「出力書式」->「申込書一覧」にて設定してください。"
ERROR_SETTING_NO_SUBSCRIPTION_CONFIRM = "申込確認書の出力書式が設定されていません、管理サイトで「出力書式」->「申込確認書一覧」にて設定してください。"
ERROR_REQUEST_SIGNATURE = "サインしてください。"
ERROR_PREV_TASK_UNFINISHED = '前のタスクは処理していないので、完了できません！'
