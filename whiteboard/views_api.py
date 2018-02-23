from django.contrib.contenttypes.models import ContentType
from django.db.models import Q
from django.shortcuts import reverse

from rest_framework import viewsets, status
from rest_framework.response import Response

from . import models, serializers
from contract.models import Subscription, Contractor


class WhiteBoardViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = models.WhiteBoard.objects.all()
    serializer_class = serializers.WhiteBoardSerializer


class WhiteBoardPositionViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = models.WhiteBoardPosition.objects.all()
    serializer_class = serializers.WhiteBoardPositionSerializer
    filter_fields = ('whiteboard__code',)


class InquiryViewSet(viewsets.ModelViewSet):
    queryset = models.Inquiry.objects.public_all()
    serializer_class = serializers.InquirySerializer


class SearchEndUserViewSet(viewsets.ViewSet):

    def list(self, request):
        name = request.GET.get('search', None)
        name_list = []
        if name:
            # 申込者
            queryset = Subscription.objects.public_filter(name__icontains=name)
            content_type = ContentType.objects.get(app_label="contract", model="subscription")
            for obj in queryset:
                d = {
                    'id': obj.pk,
                    'label': obj.name,
                    'content_type_id': content_type.pk,
                    'content_type_name': Subscription._meta.verbose_name,
                }
                name_list.append(d)
            # 契約者
            queryset = Contractor.objects.public_filter(name__icontains=name)
            content_type = ContentType.objects.get(app_label="contract", model="contractor")
            for obj in queryset:
                d = {
                    'id': obj.pk,
                    'label': obj.name,
                    'content_type_id': content_type.pk,
                    'content_type_name': Contractor._meta.verbose_name,
                }
                name_list.append(d)
            # 空き待ち
            queryset = models.Waiting.objects.public_filter(user_name__icontains=name)
            content_type = ContentType.objects.get(app_label="whiteboard", model="waiting")
            for obj in queryset:
                d = {
                    'id': obj.pk,
                    'label': obj.user_name,
                    'content_type_id': content_type.pk,
                    'content_type_name': models.Waiting._meta.verbose_name,
                }
                name_list.append(d)
            # 問い合わせ履歴
            queryset = models.Inquiry.objects.public_filter(user_name__icontains=name)
            content_type = ContentType.objects.get(app_label="whiteboard", model="inquiry")
            for obj in queryset:
                d = {
                    'id': obj.pk,
                    'label': obj.user_name,
                    'content_type_id': content_type.pk,
                    'content_type_name': models.Inquiry._meta.verbose_name,
                }
                name_list.append(d)
        return Response(name_list)


class SearchTel(viewsets.ViewSet):

    def list(self, request):
        tel = request.GET.get('search', None)
        no_list = []
        if tel:
            # 問い合わせ履歴
            queryset = models.Inquiry.objects.public_filter(tel__endswith=tel)
            for obj in queryset:
                d = {
                    'id': obj.pk,
                    'label': '問い合わせ履歴:%s %s' % (obj.tel, obj.user_name),
                    'label_value': obj.tel,
                    'url': reverse('whiteboard:inquiry_detail', args=(obj.pk,)),
                }
                no_list.append(d)
            # 契約者
            queryset = Contractor.objects.public_filter(
                Q(tel__endswith=tel) | Q(personal_phone__endswith=tel) |
                Q(corporate_staff_tel__endswith=tel) |
                Q(corporate_staff_phone__endswith=tel) |
                Q(corporate_user_tel__endswith=tel) |
                Q(workplace_tel__endswith=tel) |
                Q(contact_tel__endswith=tel) |
                Q(delivery_tel__endswith=tel) |
                Q(guarantor_tel__endswith=tel)
            )
            for obj in queryset:
                d = {
                    'id': obj.pk,
                    'label': '契約者:%s %s' % (obj.tel, obj.name),
                    'label_value': obj.tel,
                    'url': reverse('contract:contractor_detail', args=(obj.pk,)),
                }
                no_list.append(d)
            # 申込者
            queryset = Subscription.objects.public_filter(
                Q(tel__endswith=tel) | Q(personal_phone__endswith=tel) |
                Q(corporate_staff_tel__endswith=tel) |
                Q(corporate_staff_phone__endswith=tel) |
                Q(corporate_user_tel__endswith=tel) |
                Q(workplace_tel__endswith=tel) |
                Q(contact_tel__endswith=tel) |
                Q(delivery_tel__endswith=tel) |
                Q(guarantor_tel__endswith=tel),
                status__lt='11',
            )
            for obj in queryset:
                d = {
                    'id': obj.pk,
                    'label': '申込者:%s %s' % (obj.tel, obj.name),
                    'label_value': obj.tel,
                    'url': reverse('contract:subscription_detail', args=(obj.pk,)),
                }
                no_list.append(d)

        return Response(no_list)


class WaitingViewSet(viewsets.ModelViewSet):
    queryset = models.Waiting.objects.public_all()
    serializer_class = serializers.WaitingSerializer

    def create(self, request, *args, **kwargs):
        data = dict(request.data)
        data['created_user'] = request.user.pk
        for key in data.keys():
            val = data.get(key, None)
            if val and isinstance(val, list):
                data[key] = val[0] if len(val) > 0 else None
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
