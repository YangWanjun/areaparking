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
CONFIG_GROUP_GOOGLE = 'google'
CONFIG_GROUP_YAHOO = 'yahoo'
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
CONFIG_GOOGLE_MAP_KEY = 'google_map_key'
CONFIG_YAHOO_APP_KEY = 'yahoo_app_id'
CONFIG_FURIGANA_SERVICE_URL = 'furigana_service_url'
CONFIG_PARKING_LOT_KEY_ALERT_PERCENT = 'parking_lot_key_alert_percent'
CONFIG_SIMPLE_SUBSCRIPTION_PERSIST_TIME = 'simple_subscription_persist_time'

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
    ('1', "普通預金"),
    ('2', "定期預金"),
    ('3', "総合口座"),
    ('4', "当座預金"),
    ('5', "貯蓄預金"),
    ('6', "大口定期預金"),
    ('7', "積立定期預金")
)
CHOICE_BANK_DEPOSIT_TYPE = (
    ('1', "普通"),
    ('2', "当座"),
    ('4', "貯蓄"),
    ('9', "その他"),
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
    ('04', 'パスワード'),
    ('05', 'その他の鍵'),
)
CHOICE_PAY_TIMING = (
    ('10', '契約時'),
    ('11', '契約開始月'),
    ('20', '更新時'),
    ('30', '翌月以降'),
    ('40', '一時'),
    ('41', '保管場所承諾証明書発行手数料'),
    ('42', '繰越')
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
    ('04', '仮押'),
    ('05', '貸止め'),
)
CHOICE_MAIL_GROUP = (
    ('010', '申込み用フォーム送付'),
    ('011', '申込み用フォーム入力完了'),
    ('012', '審査用フォーム送付'),
    ('013', '審査用フォーム入力完了'),
    ('040', '契約フォーム送付'),
    ('041', '契約フォーム入力完了'),
    ('042', '契約書送付'),
    ('060', '鍵類、操作説明書、配置図送付'),
    ('310', '一般解約書類送付'),
    ('322', '物件解約書類送付'),
    ('800', 'バッチ：鍵残件数アラート'),
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
    ('20', '支払方法変更'),
    # ('21', '名義変更'),
    ('22', '車室変更'),
    ('23', '車両変更'),
    ('24', '鍵紛失'),
    ('25', '保管場所使用承諾証明書発行'),
    ('26', '値上げ更新'),
    ('27', '任意保険・自賠責保険更新'),
    ('28', '返金'),
    ('31', '解約'),
    ('32', '物件解約(承継なし)'),
    ('33', '物件解約(承継あり)'),
)
CHOICE_TASK_SUBSCRIPTION_CATEGORY = [
    # 01 申込
    ('010', '申込み用フォーム送付'),
    ('011', '申込み情報確認'),
    ('012', '審査用フォーム送付'),
    # 03 審査
    # ('030', '住所・電話番号 審査・確認'),
    ('031', '勤め先審査'),
    ('032', '車両サイズ審査'),
    # ('033', '申込ルート元審査'),
    ('034', '書類審査'),
    # 契約
    ('040', '契約フォーム送付'),
    ('041', '契約情報確認'),
    ('042', '契約書送付'),
    # 入金
    ('050', '入金確認'),
    ('060', '鍵類、操作説明書、配置図送付'),
]
CHOICE_TASK_CREDIT_CATEGORY = [
    ('200', '決済申込書発行'),
    ('201', '決済申込書確認'),
]
# CHOICE_TASK_NAME_CATEGORY = [
#     ('210', '契約書及び請求書の発行'),
#     ('211', '入金確認'),
#     ('212', '新契約書・請求書の送付'),
#     ('213', '結果確認'),
# ]
CHOICE_TASK_CHANGE_POSITION = [
    ('220', '契約書等送付'),
    ('221', '書類確認'),
]
CHOICE_TASK_CHANGE_CAR = [
    ('230', '書類発行'),
]
CHOICE_TASK_KEY_LOST = [
    ('240', '｢落し物｣の有無確認'),
    ('241', '書類発行'),
    ('242', '入金確認'),
    ('243', '必要書類一式と操作鍵類の送付'),
    ('244', '操作鍵類の見積り依頼（オーナー側）'),
    ('245', '操作鍵類の発注/入金'),
]
CHOICE_TASK_PRICE_RAISE = [
    ('260', '更新書類の発行'),
    ('261', '更新書類の確認'),
]
CHOICE_TASK_CONTRACT_CANCELLATION = [
    ('310', '退出届送付'),
    ('311', '解約処理'),
    ('312', '鍵返送案内'),
    ('313', '鍵回収'),
]
CHOICE_TASK_POSITION_CANCELLATION_WITHOUT_CONTINUE = [
    ('320', '代替駐車場の調査'),
    ('321', 'ユーザーへ連絡'),
    ('322', '強制解約書類送付'),
    ('323', '滞納金確認'),
    ('324', '返金確認'),
    ('325', '鍵返送案内'),
    ('326', '鍵回収'),
]
CHOICE_TASK_POSITION_CANCELLATION_WITH_CONTINUE = [
    ('330', 'ユーザーへ連絡'),
    ('331', '承継承諾書送付'),
    ('332', '滞納金確認'),
    ('333', '返金確認'),
    ('334', '予備分の操作鍵類と契約時書類オーナー側へ送付'),
]
CHOICE_TASK_CATEGORY = CHOICE_TASK_SUBSCRIPTION_CATEGORY + \
                       CHOICE_TASK_CREDIT_CATEGORY + \
                       CHOICE_TASK_CHANGE_POSITION + \
                       CHOICE_TASK_CHANGE_CAR + \
                       CHOICE_TASK_KEY_LOST + \
                       CHOICE_TASK_PRICE_RAISE + \
                       CHOICE_TASK_CONTRACT_CANCELLATION + \
                       CHOICE_TASK_POSITION_CANCELLATION_WITHOUT_CONTINUE + \
                       CHOICE_TASK_POSITION_CANCELLATION_WITH_CONTINUE
CHOICE_TASK_STATUS = (
    ('01', '未実施'),
    ('02', '実施中'),
    ('10', 'スキップ'),
    ('20', '見送る'),
    ('99', '完了'),
)
CHOICE_CONTRACT_STATUS = (
    ('01', '仮契約'),
    ('11', '本契約'),
    ('21', '破棄'),
)
CHOICE_SUBSCRIPTION_STATUS = (
    ('01', '新規申込'),
    ('02', '申込フォーム送付済'),
    ('03', '申込フォーム入力完了'),
    ('04', '審査フォーム送付済'),
    ('05', '審査フォーム入力完了'),
    ('06', '契約フォーム送付済'),
    ('07', '契約フォーム入力完了'),
    ('08', '契約書送付済'),
    ('09', '鍵類、操作説明書、配置図送付済'),
    ('11', '成約'),
    ('12', '破棄'),
)
CHOICE_INSURANCE_JOIN_STATUS = (
    ('within', '加入中'),
    ('without', '加入なし'),
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
CHOICE_TRANSFER_STATUS = (
    ('00', '請求なし'),
    ('01', '金額不一致'),
    ('02', '名義不一致'),
    ('03', '繰越'),
    ('11', '完全一致'),
    ('99', 'その他'),
)
CHOICE_PAYMENT_KBN = (
    ('01', '振込'),
    ('02', '振替'),
    ('03', 'クレジット'),
)
CHOICE_WAITING_STATUS = (
    ('01', '新規'),
    ('10', '成約'),
    ('90', 'キャンセル'),
)
CHOICE_BANK_ACCOUNT_STATUS = (
    ('0', '使用なし'),
    ('1', '使用中'),
)

ERROR_SETTING_NO_SUBSCRIPTION = "申込書の出力書式が設定されていません、管理サイトで「出力書式」->「申込書一覧」にて設定してください。"
ERROR_SETTING_NO_SUBSCRIPTION_CONFIRM = "申込確認書の出力書式が設定されていません、管理サイトで「出力書式」->「申込確認書一覧」にて設定してください。"
ERROR_REQUEST_SIGNATURE = "サインしてください。"
ERROR_PREV_TASK_UNFINISHED = '前のタスクは処理していないので、完了できません！'
ERROR_SUBSCRIPTION_NO_CAR = '車情報がありません。'
ERROR_SUBSCRIPTION_LOCKED = '貸止めになっているため、申込みはできません。'
ERROR_SUBSCRIPTION_CONTRACTED = "既に契約中なので、申込みはできません。"
ERROR_SUBSCRIPTION_PROCESS_NOT_FINISHED = "契約手続きはまだ完了されていません。"
ERROR_SUBSCRIPTION_EMAIL_CONFIRM = "メールアドレスとメールアドレス（確認）は不一致です。"
ERROR_SUBSCRIPTION_PRIVACY_AGREEMENT = "プライバシーポリシーおよび利用規約に承諾してください。"
ERROR_CONTRACT_WRONG_RETIRE_DATE = "退居予定日は解約日の前に選択してください。"
ERROR_CONTRACT_RETIRE_DATE_RANGE = "退居予定日は契約期間内に選択してください。"
ERROR_CONTRACT_CANCELLATION_DATE_RANGE = "解約日は契約期間内に選択してください。"
ERROR_PARKING_LOT_CANCELLATION_NO_POSITIONS = "物件解約の場合全体解約または車室を選択してください。"
ERROR_FORMAT_BANK_TRANSFER = "全銀フォーマットエラー。"
ERROR_FORMAT_BANK_TRANSFER_CANNOT_IMPORT = "ファイル読み込みできません。"
ERROR_REQUIRE_TRANSFER_DATA = "入金データを選択してください。"
ERROR_REQUIRED_FIELD = "%s は必須項目です。"