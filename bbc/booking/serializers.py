from rest_framework import serializers
from . import models


# class StatusSerializer(serializers.ModelSerializer):
#     court_id = serializers.StringRelatedField(
#         read_only=True, allow_null=True)

#     court_num = serializers.StringRelatedField(
#         read_only=True, allow_null=True)

#     class Meta:
#         model = models.Status
#         fields = ('court_id', 'court_num',  'name', 'time', 'time_out')


class EachCourtInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.EachCourtInfo
        fields = ('court_number', 'price_normal', 'price_ds_mem',
                  'price_ds_time', 'time_ds_start', 'time_ds_end')
