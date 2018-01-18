from django.contrib.auth.models import User
from django.db import models
from django.utils.functional import cached_property

from contract.models import Contract, Contractor, ParkingLot, ParkingPosition, ContractPayment
from master.models import BankAccount
from utils import constants, errors
from utils.django_base import BaseModel, BaseViewModel


# Create your models here.
class TransferDebitHeader(BaseModel):
    company_code = models.CharField(max_length=10, verbose_name="会社コード")
    company_name = models.CharField(max_length=40, verbose_name="依頼人名")
    transfer_md = models.CharField(max_length=4, verbose_name="振込指定日")
    bank_code = models.CharField(max_length=4, verbose_name="仕向金融機関コード")
    bank_name = models.CharField(max_length=15, verbose_name="仕向金融機関名")
    branch_no = models.CharField(max_length=3, verbose_name="仕向店舗コード")
    branch_name = models.CharField(max_length=15, verbose_name="仕向店舗名")
    account_number = models.CharField(max_length=7, verbose_name="依頼人口座番号")

    class Meta:
        db_table = 'ap_transfer_debit_header'
        verbose_name = "引き落し"
        verbose_name_plural = "引き落し一覧"

    def __str__(self):
        return self.company_name

    @classmethod
    def parse_header(cls, text):
        """読み込んだ文字列を振替ヘッダー情報に変更する。

        :param text:
        :return:
        """
        if text and len(text) == 120 and text[0] == '1':
            header = TransferDebitHeader()
            header.company_code = text[4:14]
            header.company_name = text[14:54]
            header.transfer_md = text[54:58]
            header.bank_code = text[58:62]
            header.bank_name = text[62:77]
            header.branch_no = text[77:80]
            header.branch_name = text[80:95]
            header.account_number = text[96:103]
            return header
        else:
            raise errors.CustomException(constants.ERROR_FORMAT_BANK_TRANSFER)

    def parse_detail(self, text):
        """読み込んだ文字列を振替明細情報に変更する。

        :param text:
        :return:
        """
        if text and len(text) == 120 and text[0] == '2':
            detail = TransferDebitDetail(header=self)
            detail.bank_code = text[1:5]
            detail.bank_name = text[5:20]
            detail.branch_no = text[20:23]
            detail.branch_name = text[23:38]
            detail.deposit_type = text[42]
            detail.account_number = text[43:50]
            detail.account_holder = text[50:80]
            detail.amount = int(text[80:90])
            detail.customer_code = text[91:111]
            return detail
        else:
            raise errors.CustomException(constants.ERROR_FORMAT_BANK_TRANSFER)


class TransferDebitDetail(BaseModel):
    debit_header = models.ForeignKey(TransferDebitHeader, on_delete=models.PROTECT, verbose_name="振替ヘッダー")
    bank_code = models.CharField(max_length=4, verbose_name="振込先金融機関コード")
    bank_name = models.CharField(max_length=15, verbose_name="振込先金融機関名称")
    branch_no = models.CharField(max_length=3, verbose_name="振込先営業店コード")
    branch_name = models.CharField(max_length=15, verbose_name="振込先営業店名称")
    deposit_type = models.CharField(max_length=1, choices=constants.CHOICE_BANK_DEPOSIT_TYPE, verbose_name="振込先の科目")
    account_number = models.CharField(max_length=7, verbose_name="振込先の口座番号")
    account_holder = models.CharField(max_length=30, verbose_name="受取人名(カナ)")
    amount = models.IntegerField(verbose_name="振込金額")
    customer_code = models.CharField(max_length=20, verbose_name="顧客ｺｰﾄﾞ（社員番号）")

    class Meta:
        db_table = 'ap_transfer_debit_detail'
        verbose_name = "引き落し明細"
        verbose_name_plural = "引き落し明細一覧"

    def __str__(self):
        return self.account_holder


class TransferHeader(BaseModel):
    data_kbn = models.CharField(max_length=1, verbose_name="データ区分", help_text="レコード種別")
    category = models.CharField(max_length=2, verbose_name="種別コード", help_text="業務種類別区分")
    code_kbn = models.CharField(max_length=1, verbose_name="コード区分", help_text="文字コード種別")
    created_ymd = models.CharField(max_length=6, verbose_name="作成日", help_text="ファイル作成日(和暦)")
    settlement_from = models.CharField(max_length=6, verbose_name="勘定日(自)", help_text="最古の取引日(自)　(和暦)")
    settlement_to = models.CharField(max_length=6, verbose_name="勘定日(至)", help_text="取引日(至)　(和暦)")
    bank_code = models.CharField(max_length=4, verbose_name="取引銀行コード")
    bank_name = models.CharField(max_length=15, verbose_name="取引銀行名")
    branch_no = models.CharField(max_length=3, verbose_name="取引支店コード")
    branch_name = models.CharField(max_length=15, verbose_name="取引支店名")
    dummy1 = models.CharField(max_length=3, verbose_name="ダミー")
    deposit_type = models.CharField(max_length=1, verbose_name="預金種目", help_text="照会口座の預金科目")
    account_number = models.CharField(max_length=10, verbose_name="口座番号", help_text="照会口座の口座番号")
    account_holder = models.CharField(max_length=40, verbose_name="口座名", help_text="照会口座の口座名義")
    overdraft_kbn = models.CharField(max_length=1, verbose_name="貸越区分", help_text="取引前の貸越区分 1…プラス　2…マイナス")
    passbook_kbn = models.CharField(max_length=1, verbose_name=" 通帳・証書区分", help_text="取引が通帳によるか証書によるか 1…通帳　2…証書")
    balance = models.CharField(max_length=14, verbose_name="取引前残高", help_text="取引前残高")
    dummy2 = models.CharField(max_length=71, verbose_name="ダミー")
    raw_text = models.CharField(max_length=200, verbose_name="元データ")
    import_user = models.ForeignKey(User, verbose_name="導入ユーザー")

    class Meta:
        db_table = 'ap_transfer_header'
        verbose_name = "振込み"
        verbose_name_plural = "振込み一覧"

    def __str__(self):
        return self.created_ymd

    @classmethod
    def is_header(cls, text):
        if text and len(text) == 200 and text[0] == '1':
            return True
        else:
            return False

    @classmethod
    def is_detail(cls, text):
        if text and len(text) == 200 and text[0] == '2':
            return True
        else:
            return False

    @classmethod
    def parse_header(cls, text, user):
        """読み込んだ文字列を振替ヘッダー情報に変更する。

        :param text:
        :return:
        """
        if cls.is_header(text):
            header = TransferHeader()
            header.data_kbn = text[0]
            header.category = text[1:3]
            header.code_kbn = text[3]
            header.created_ymd = text[4:10]
            header.settlement_from = text[10:16]
            header.settlement_to = text[16:22]
            header.bank_code = text[22:26]
            header.bank_name = text[26:41]
            header.branch_no = text[41:44]
            header.branch_name = text[44:59]
            header.dummy1 = text[59:62]
            header.deposit_type = text[62]
            header.account_number = text[63:73]
            header.account_holder = text[73:113]
            header.overdraft_kbn = text[113]
            header.passbook_kbn = text[114]
            header.balance = int(text[115:129])
            header.dummy2 = text[129:]
            header.raw_text = text
            header.import_user = user
            return header
        else:
            raise errors.CustomException(constants.ERROR_FORMAT_BANK_TRANSFER)

    def parse_detail(self, text):
        """読み込んだ文字列を振替明細情報に変更する。

        :param text:
        :return:
        """
        if self.is_detail(text):
            detail = TransferDetail(header=self)
            detail.data_kbn = text[0]
            detail.reference_no = text[1:9]
            detail.settlement_ymd = text[9:15]
            detail.reckoning_ymd = text[15:21]
            detail.in_out_kbn = text[21]
            detail.trade_kbn = text[22:24]
            detail.amount = int(text[24:36])
            detail.other_amount = int(text[36:48])
            detail.exchange_ymd = text[48:54]
            detail.return_ymd = text[54:60]
            detail.check_kbn = text[60]
            detail.check_no = text[61:68]
            detail.branch_no = text[68:71]
            detail.nominee_code = text[71:81]
            detail.nominee_name = text[81:129]
            detail.bank_name = text[129:144]
            detail.branch_name = text[144:159]
            detail.summary = text[159:179]
            detail.edi_info = text[179:199]
            detail.dummy1 = text[199]
            detail.raw_text = text
            return detail
        else:
            raise errors.CustomException(constants.ERROR_FORMAT_BANK_TRANSFER)


class TransferDetail(BaseModel):
    header = models.ForeignKey(TransferHeader, on_delete=models.PROTECT, verbose_name="振込ヘッダー")
    data_kbn = models.CharField(max_length=1, verbose_name="データ区分", help_text="レコード種別")
    reference_no = models.CharField(max_length=8, verbose_name="照会番号")
    settlement_ymd = models.CharField(max_length=6, verbose_name="勘定日")
    reckoning_ymd = models.CharField(max_length=6, verbose_name="預入・払出日", help_text="入金・出金の起算日　(和暦)")
    in_out_kbn = models.CharField(max_length=1, verbose_name="入払区分", help_text="入出金の状態を表す区分")
    trade_kbn = models.CharField(max_length=2, verbose_name="取引区分", help_text="2 取引形態を表す区分")
    amount = models.IntegerField(verbose_name="金額")
    other_amount = models.IntegerField(verbose_name="うち他店券金額", help_text="入金金額のうち、他店券の金額")
    exchange_ymd = models.CharField(max_length=6, blank=True, null=True, verbose_name="交換提示日")
    return_ymd = models.CharField(max_length=6, blank=True, null=True, verbose_name="不渡返還日 ")
    check_kbn = models.CharField(max_length=1, blank=True, null=True, verbose_name="手形・小切手区分")
    check_no = models.CharField(max_length=7, blank=True, null=True, verbose_name="手形・小切手番号")
    branch_no = models.CharField(max_length=3, verbose_name="僚店番号")
    nominee_code =models.CharField(max_length=10, verbose_name="振込依頼人コード")
    nominee_name =models.CharField(max_length=48, verbose_name="振込依頼人名等")
    bank_name = models.CharField(max_length=15, verbose_name="仕向銀行名", help_text="仕向(振込元)金融機関名")
    branch_name = models.CharField(max_length=15, verbose_name="仕向店名", help_text="仕向(振込元)支店名")
    summary = models.CharField(max_length=20, verbose_name="摘要内容")
    edi_info = models.CharField(max_length=20, blank=True, null=True, verbose_name="EDI情報")
    dummy1 = models.CharField(max_length=1, blank=True, null=True, verbose_name="ダミー")
    raw_text = models.CharField(max_length=200, verbose_name="元データ")

    class Meta:
        db_table = 'ap_transfer_detail'
        verbose_name = "振込明細"
        verbose_name_plural = "振込明細一覧"

    def __str__(self):
        return self.nominee_name

    @cached_property
    def requests(self):
        account_number = self.nominee_code[3:]
        year = '2017'
        month = self.reckoning_ymd[2:4]
        return Request.objects.public_filter(bank_account__account_number=account_number, year=year, month=month)


class Request(BaseModel):
    year = models.CharField(max_length=4, verbose_name="請求年")
    month = models.CharField(max_length=2, verbose_name="請求月")
    bank_account = models.ForeignKey(BankAccount, verbose_name="口座")
    amount = models.IntegerField(verbose_name="請求金額")
    contract_payment = models.ForeignKey(ContractPayment, verbose_name="入金項目")

    class Meta:
        db_table = 'ap_request'
        verbose_name = "請求"
        verbose_name_plural = "請求一覧"

    def __str__(self):
        return str(self.pk)


class ContractorTransfer(BaseModel):
    contractor = models.ForeignKey(Contractor, on_delete=models.PROTECT, verbose_name="契約者")
    transfer_detail = models.ForeignKey(TransferDetail, on_delete=models.PROTECT, verbose_name="振込明細")

    class Meta:
        db_table = 'ap_contractor_transfer'
        verbose_name = "契約者入金"
        verbose_name_plural = "契約者入金履歴"

    def __str__(self):
        return str(self.contractor)


class VTransferDetail(BaseViewModel):
    header = models.ForeignKey(TransferHeader, on_delete=models.DO_NOTHING, verbose_name="振込ヘッダー")
    detail = models.ForeignKey(TransferDetail, on_delete=models.DO_NOTHING, verbose_name="振込明細")
    reference_no = models.CharField(max_length=8, verbose_name="照会番号")
    settlement_ymd = models.CharField(max_length=6, verbose_name="勘定日")
    reckoning_ymd = models.CharField(max_length=6, verbose_name="預入・払出日", help_text="入金・出金の起算日　(和暦)")
    in_out_kbn = models.CharField(max_length=1, verbose_name="入払区分", help_text="入出金の状態を表す区分")
    trade_kbn = models.CharField(max_length=2, verbose_name="取引区分", help_text="2 取引形態を表す区分")
    amount = models.IntegerField(verbose_name="金額")
    other_amount = models.IntegerField(verbose_name="うち他店券金額", help_text="入金金額のうち、他店券の金額")
    exchange_ymd = models.CharField(max_length=6, blank=True, null=True, verbose_name="交換提示日")
    return_ymd = models.CharField(max_length=6, blank=True, null=True, verbose_name="不渡返還日 ")
    check_kbn = models.CharField(max_length=1, blank=True, null=True, verbose_name="手形・小切手区分")
    check_no = models.CharField(max_length=7, blank=True, null=True, verbose_name="手形・小切手番号")
    branch_no = models.CharField(max_length=3, verbose_name="僚店番号")
    nominee_code =models.CharField(max_length=10, verbose_name="振込依頼人コード")
    nominee_name =models.CharField(max_length=48, verbose_name="振込依頼人名等")
    bank_name = models.CharField(max_length=15, verbose_name="仕向銀行名", help_text="仕向(振込元)金融機関名")
    branch_name = models.CharField(max_length=15, verbose_name="仕向店名", help_text="仕向(振込元)支店名")
    summary = models.CharField(max_length=20, verbose_name="摘要内容")
    request = models.ForeignKey(Request, blank=True, null=True, on_delete=models.DO_NOTHING, verbose_name="請求")
    request_amount = models.IntegerField(blank=True, null=True, verbose_name="金額")
    contract = models.OneToOneField(Contract, blank=True, null=True, on_delete=models.DO_NOTHING, verbose_name="契約情報")
    parking_lot = models.ForeignKey(ParkingLot, blank=True, null=True, on_delete=models.DO_NOTHING, verbose_name="駐車場")
    parking_position = models.ForeignKey(ParkingPosition, blank=True, null=True, on_delete=models.DO_NOTHING,
                                         verbose_name="車室番号")
    contractor = models.ForeignKey(Contractor, blank=True, null=True, on_delete=models.DO_NOTHING, verbose_name="契約者")
    status = models.CharField(max_length=2, choices=constants.CHOICE_TRANSFER_STATUS, verbose_name="状態")
    is_committed = models.BooleanField(default=False, verbose_name="入金済み")

    class Meta:
        managed = False
        db_table = 'v_transfer_detail'
        verbose_name = "振込明細"
        verbose_name_plural = "振込明細一覧"

    def __str__(self):
        return self.nominee_name

    @cached_property
    def transfer_kana_list(self):
        if self.contractor:
            queryset = ContractorTransfer.objects.public_filter(
                contractor=self.contractor
            ).values('transfer_detail__nominee_name')
            return [item.get('transfer_detail__nominee_name') for item in queryset]
        else:
            return []


class VContractorRequest(BaseViewModel):
    contractor = models.ForeignKey(Contractor, on_delete=models.DO_NOTHING, verbose_name="契約者")
    name = models.CharField(max_length=30, verbose_name="名前")
    request = models.ForeignKey(Request, blank=True, null=True, on_delete=models.DO_NOTHING, verbose_name="請求")

    class Meta:
        managed = False
        db_table = 'v_contractor_request'
        verbose_name = "契約者別請求"
        verbose_name_plural = "契約者別請求一覧"

    def __str__(self):
        return self.name
