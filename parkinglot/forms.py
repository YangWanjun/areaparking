from django import forms
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Max

from . import models
from utils import constants, common, errors
from utils.django_base import BaseForm


class ParkingLotForm(BaseForm):
    class Meta:
        model = models.ParkingLot
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(ParkingLotForm, self).__init__(*args, **kwargs)
        self.fields['name'].widget.attrs.update({'onchange': "ebjs.material.set_furigana(this, 'id_kana')"})
        self.fields['time_limit_comment'].widget = forms.Textarea()
        self.fields['transit_pass_comment'].widget = forms.Textarea()
        self.fields['lease_management_company'].widget.attrs.update({
            'data-initial': "true",
            'onchange': "ebjs.material.set_related_management_company_staff(this, 'id_lease_management_company_staff')"
        })
        self.fields['building_management_company'].widget.attrs.update({
            'data-initial': "true",
            'onchange': "ebjs.material.set_related_management_company_staff(this, 'id_building_management_company_staff')"
        })
        # if self.instance:
        #     # 賃貸管理会社
        #     if self.instance.lease_management_company:
        #         self.fields['lease_management_company_staff'].queryset \
        #             = models.ManagementCompanyStaff.objects.public_filter(company=self.instance.lease_management_company)
        #     else:
        #         self.fields['lease_management_company_staff'].queryset = models.ManagementCompanyStaff.objects.none()
        #     # 建物管理会社
        #     if self.instance.building_management_company:
        #         self.fields['building_management_company_staff'].queryset \
        #             = models.ManagementCompanyStaff.objects.public_filter(company=self.instance.building_management_company)
        #     else:
        #         self.fields['building_management_company_staff'].queryset = models.ManagementCompanyStaff.objects.none()

    def clean(self):
        cleaned_data = super(ParkingLotForm, self).clean()
        staff_start_date = cleaned_data.get('staff_start_date', None)
        # 担当者変更時のチェック
        if self.has_changed() and ('staff' in self.changed_data or 'staff_start_date' in self.changed_data) \
                and staff_start_date != self.instance.staff_start_date:
            queryset = models.ParkingLotStaffHistory.objects.public_filter(parking_lot=self.instance)
            try:
                history_end_date = queryset.aggregate(Max('end_date')).get('end_date__max', None)
                # 担当開始日は履歴の終了日より以前の場合はエラー発生とする。
                if history_end_date and history_end_date >= staff_start_date:
                    self.add_error('staff_start_date', constants.ERROR_PARKING_LOT_INVALID_STAFF_START_DATE)
            except ObjectDoesNotExist:
                self.add_error('code', constants.ERROR_PARKING_LOT_NOT_EXISTS)
        return cleaned_data


class ParkingPositionForm(BaseForm):
    class Meta:
        model = models.ParkingPosition
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        forms.ModelForm.__init__(self, *args, **kwargs)
        if self.instance and self.instance.pk:
            self.fields['parking_lot'].queryset = models.ParkingLot.objects.filter(pk=self.instance.parking_lot.pk)
        else:
            self.fields['parking_lot'].queryset = models.ParkingLot.objects.public_all().order_by('-created_date')
        # 税金自動計算
        self.fields['price_recruitment_no_tax'].widget.attrs.update({
            'onchange': "ebjs.material.set_tax_included(this, 'id_price_recruitment')"
        })
        self.fields['price_homepage_no_tax'].widget.attrs.update({
            'onchange': "ebjs.material.set_tax_included(this, 'id_price_homepage')"
        })
        self.fields['price_handbill_no_tax'].widget.attrs.update({
            'onchange': "ebjs.material.set_tax_included(this, 'id_price_handbill')"
        })

    def clean(self):
        cleaned_data = super(ParkingPositionForm, self).clean()
        name = cleaned_data.get('name', None)
        if self.instance and self.instance.pk:
            # 変更の場合、数字しかン入力できないように
            if not common.is_number(name):
                self.add_error('name', constants.ERROR_PARKING_POSITION_NAME_NUMBER)
        else:
            # 追加の場合
            try:
                # 連番の場合、終了番号は開始番号より小さい場合エラー発生する。
                common.get_continued_positions(name)
            except errors.CustomException as ex:
                self.add_error('name', ex.message)
        return cleaned_data


class ParkingLotDocForm(BaseForm):
    class Meta:
        model = models.ParkingLotDoc
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        forms.ModelForm.__init__(self, *args, **kwargs)
        self.fields['path'].widget.attrs.update({'class': "change_comment"})
