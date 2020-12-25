from rest_framework import serializers
from . import models


class MemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Member
        fields = ('username', 'first_name', 'last_name',
                  'email', 'tel', 'birthday', 'gender', 'mygroup')


# class RequestSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = models.Request
#         fields = ('sender', 'action', 'state',
#                   'email', 'tel', 'birthday', 'gender', 'mygroup')
