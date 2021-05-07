from rest_framework import serializers
from . import models
from datetime import datetime as dt


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


class EachCourtInfo2Serializer(serializers.ModelSerializer):
    class Meta:
        model = models.EachCourtInfo
        fields = ('court_number', 'price_normal', 'price_ds_group',
                  'price_ds_time', 'time_ds_start', 'time_ds_end')


class PaymentSerializer(serializers.ModelSerializer):
    number = serializers.IntegerField(allow_null=True)

    class Meta:
        model = models.Payment
        # fields = ('__all__')
        exclude = ('id', 'member', 'group')


class HistorySerializer(serializers.ModelSerializer):

    number = serializers.IntegerField(allow_null=True)
    court = serializers.IntegerField(source='court.court_number')
    date = serializers.DateTimeField(
        source='booking_datetime', format="%Y-%m-%d")
    time = serializers.DateTimeField(
        source='booking_datetime', format="%H:%M:%S")

    class Meta:
        model = models.Booking
        fields = ('number', 'date', 'court', 'time', 'bookingid')
        # fields = ('court__court_number',)
