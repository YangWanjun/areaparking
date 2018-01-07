from rest_framework import serializers

from . import models


class MemberSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField()

    class Meta:
        model = models.Member
        fields = ('id', 'first_name', 'last_name', 'full_name')

    def get_full_name(self, obj):
        return "{} {}".format(obj.first_name, obj.last_name)
