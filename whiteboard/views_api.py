from rest_framework import viewsets

from . import models, serializers


class WhiteBoardViewSet(viewsets.ModelViewSet):
    queryset = models.WhiteBoard.objects.all()
    serializer_class = serializers.WhiteBoardSerializer


class InquiryViewSet(viewsets.ModelViewSet):
    queryset = models.Inquiry.objects.public_all()
    serializer_class = serializers.InquirySerializer
