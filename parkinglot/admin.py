import datetime

from django.contrib import admin
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Max

from . import models, forms
from address.biz import geocode
from utils import common
from utils.django_base import BaseAdmin


# Register your models here.
class ParkingPositionInline(admin.TabularInline):
    model = models.ParkingPosition
    extra = 0


class ParkingLotDocInline(admin.TabularInline):
    model = models.ParkingLotDoc
    form = forms.ParkingLotDocForm
    extra = 0


class ParkingLotImageInline(admin.TabularInline):
    model = models.ParkingLotImage
    extra = 0


class ParkingLotCommentInline(admin.TabularInline):
    model = models.ParkingLotComment
    extra = 0


class ParkingLotKeyInline(admin.TabularInline):
    model = models.ParkingLotKey
    extra = 0


class ParkingLotStaffHistoryInline(admin.TabularInline):
    model = models.ParkingLotStaffHistory
    extra = 0

    def has_add_permission(self, request):
        return False

    # def has_delete_permission(self, request, obj=None):
    #     return False


class ParkingPositionKeyInline(admin.TabularInline):
    model = models.ParkingPositionKey
    extra = 0


class ManagementCompanyStaffInline(admin.TabularInline):
    model = models.ManagementCompanyStaff
    extra = 0


@admin.register(models.ParkingLotType)
class ParkingLotTypeAdmin(BaseAdmin):
    list_display = ('code', 'name')
    list_display_links = ('code', 'name')


# @admin.register(models.LeaseManagementCompany)
# class LeaseManagementCompanyAdmin(BaseAdmin):
#     list_display = ('name', 'department', 'position', 'staff', 'address', 'tel', 'email')
#
#
# @admin.register(models.BuildingManagementCompany)
# class BuildingManagementCompanyAdmin(BaseAdmin):
#     list_display = ('name', 'department', 'position', 'staff', 'address', 'tel', 'email')


@admin.register(models.ManagementCompany)
class ManagementCompanyAdmin(BaseAdmin):
    list_display = ('name', 'address', 'tel', 'email')
    inlines = (ManagementCompanyStaffInline,)


@admin.register(models.TryPuttingOperator)
class TryPuttingOperatorAdmin(BaseAdmin):
    pass


@admin.register(models.ParkingLot)
class ParkingLotAdmin(BaseAdmin):
    form = forms.ParkingLotForm
    icon = '<i class="material-icons">local_parking</i>'
    list_display = ('code', 'name', 'category', 'address', 'subscription_list_send_type')
    search_fields = ('code', 'name',)
    inlines = (ParkingLotCommentInline, ParkingLotStaffHistoryInline, ParkingLotDocInline, ParkingLotImageInline,
               ParkingLotKeyInline)

    def save_model(self, request, obj, form, change):
        if change is False or (
            'pref_name' in form.changed_data or
            'city_name' in form.changed_data or
            'town_name' in form.changed_data or
            'aza_name' in form.changed_data or
            'other_name' in form.changed_data
        ):
            # 新規の場合、または住所変更した場合、座標を取得しなおします。
            coordinate = geocode(obj.address)
            if coordinate.get('lng', None):
                obj.lng = coordinate.get('lng', None)
            if coordinate.get('lat', None):
                obj.lat = coordinate.get('lat', None)
            if coordinate.get('post_code', None):
                obj.post_code = coordinate.get('post_code', None)
        # 担当者変更時、駐車場担当者履歴追加
        if change and 'staff' in form.changed_data:
            queryset = models.ParkingLotStaffHistory.objects.public_filter(parking_lot=obj)
            try:
                last_staff = models.ParkingLot.objects.get(pk=obj.pk).staff
                last_start_date = models.ParkingLot.objects.get(pk=obj.pk).staff_start_date
                history_end_date = queryset.aggregate(Max('end_date')).get('end_date__max', None)
                if (history_end_date is None or history_end_date < obj.staff_start_date) and last_start_date != obj.staff_start_date:
                    models.ParkingLotStaffHistory.objects.create(
                        parking_lot=obj,
                        member=last_staff,
                        start_date=last_start_date,
                        end_date=(obj.staff_start_date + datetime.timedelta(days=-1))
                    )
            except ObjectDoesNotExist:
                pass
        super(ParkingLotAdmin, self).save_model(request, obj, form, change)


@admin.register(models.ParkingPosition)
class ParkingPosition(BaseAdmin):
    form = forms.ParkingPositionForm
    list_display = ('parking_lot', 'name', 'length', 'width', 'height', 'weight')
    list_display_links = ('parking_lot', 'name',)
    search_fields = ('parking_lot__code', 'parking_lot__name')
    fieldsets = (
        (None, {
            'fields': (
                'parking_lot',
                'name', 'category', 'cost',
            )
        }),
        ("賃料", {
            'classes': ('collapse',),
            'fields': (
                ('price_recruitment_no_tax', 'price_recruitment'),
                ('price_homepage_no_tax', 'price_homepage'),
                ('price_handbill_no_tax', 'price_handbill'),
            )
        }),
        ("サイズ", {
            'classes': ('collapse',),
            'fields': (
                ('length', 'width', 'height', 'weight'),
                ('tyre_width', 'tyre_width_ap', 'min_height', 'min_height_ap'),
                ('f_value', 'r_value',),
            )
        }),
        ('備考', {
            'fields': (
                'comment',
            )
        }),
    )
    inlines = (ParkingPositionKeyInline,)
    save_as = True

    def save_model(self, request, obj, form, change):
        continued_positions = common.get_continued_positions(obj.name)
        if continued_positions:
            split_positions = []
        else:
            split_positions = [s for s in obj.name.split(',') if s]
        continued_positions.extend(split_positions)
        if not change and continued_positions:
            # 複数の車室を追加の場合
            for name in continued_positions:
                if models.ParkingPosition.objects.public_filter(parking_lot=obj.parking_lot, name=name).count() == 0:
                    obj.pk = None
                    obj.name = name
                    obj.save()
        else:
            super(ParkingPosition, self).save_model(request, obj, form, change)
