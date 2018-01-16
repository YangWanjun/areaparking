from django.db import models

from utils import constants, errors
from utils.django_base import BaseModel


# Create your models here.
class TransferHeader(BaseModel):
    company_code = models.CharField(max_length=10, verbose_name="会社コード")
    company_name = models.CharField(max_length=40, verbose_name="依頼人名")
    transfer_md = models.CharField(max_length=4, verbose_name="振込指定日")
    bank_code = models.CharField(max_length=4, verbose_name="仕向金融機関コード")
    bank_name = models.CharField(max_length=15, verbose_name="仕向金融機関名")
    branch_no = models.CharField(max_length=3, verbose_name="仕向店舗コード")
    branch_name = models.CharField(max_length=15, verbose_name="仕向店舗名")
    account_number = models.CharField(max_length=7, verbose_name="依頼人口座番号")

    class Meta:
        db_table = 'mst_transfer_header'
        verbose_name = "振替ヘッダー"
        verbose_name_plural = "振替ヘッダー一覧"

    def __str__(self):
        return self.company_name

    @classmethod
    def parse_header(cls, text):
        """読み込んだ文字列を振替ヘッダー情報に変更する。

        :param text:
        :return:
        """
        if text and len(text) == 120 and text[0] == '2':
            header = TransferHeader()
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
            detail = TransferDetail(header=self)
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


class TransferDetail(BaseModel):
    header = models.ForeignKey(TransferHeader, on_delete=models.PROTECT, verbose_name="振替ヘッダー")
    bank_code = models.CharField(max_length=4, verbose_name="振込先金融機関コード")
    bank_name = models.CharField(max_length=15, verbose_name="振込先金融機関名称")
    branch_no = models.CharField(max_length=3, verbose_name="振込先営業店コード")
    branch_name = models.CharField(max_length=15, verbose_name="振込先営業店名称")
    deposit_type = models.CharField(max_length=1, choices=constants.CHOICE_BANK_DEPOSIT_TYPE, verbose_name="振込先の科目")
    account_number = models.CharField(max_length=7, verbose_name="振込先の口座番号")
    account_holder = models.CharField(max_length=30, verbose_name="受取人名(カナ)")
    amount = models.IntegerField(verbose_name="振込金額")
    customer_code = models.CharField(max_length=20, verbose_name="顧客ｺｰﾄﾞ１（社員番号）")

    class Meta:
        db_table = 'mst_transfer_detail'
        verbose_name = "振替明細"
        verbose_name_plural = "振替明細一覧"

    def __str__(self):
        return self.account_holder
