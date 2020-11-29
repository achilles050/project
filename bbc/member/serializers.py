from rest_framework import serializers
from . import models


class MemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Member
        fields = ('username', 'first_name', 'last_name',
                  'email', 'password', 'tel', 'birthday', 'gender', 'group_name')
