from django.db.models import Q
from django.shortcuts import reverse

from rest_framework import viewsets
from rest_framework.response import Response

from . import models, serializers
from contract.models import Subscription, Contractor


class WhiteBoardViewSet(viewsets.ModelViewSet):
    queryset = models.WhiteBoard.objects.all()
    serializer_class = serializers.WhiteBoardSerializer


class InquiryViewSet(viewsets.ModelViewSet):
    queryset = models.Inquiry.objects.public_all()
    serializer_class = serializers.InquirySerializer


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
