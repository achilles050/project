from rest_framework import serializers
from member import models as mem_models
from booking import models as bk_models


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = mem_models.Group
        fields = ('group_name', 'header', 'outside_detail', 'inside_detail',
                  'is_continue', 'is_active')


class GroupMemberSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = mem_models.GroupMember
        fields = ('group', 'member', 'on_court')


class MemberSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = mem_models.Member
        fields = ('username', 'first_name', 'last_name',
                  'email', 'password', 'tel', 'birthday', 'gender', 'group_name')


class CheckPaymentSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = bk_models.CheckPayment
        fields = ('history', 'ref1', 'ref2',
                  'pay', 'state', 'is_found')


class CourtDetailSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = bk_models.CourtDetail
        fields = ('id', 'court_number', 'price_normal', 'price_ds_mem',
                  'price_ds_gang', 'price_ds_time', 'time_ds_start', 'time_ds_end', 'maintain')


class OtherDetailSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = bk_models.OtherDetail
        fields = ('refund_gap_minute', 'confirm_gap_minute', 'refund_percent', 'time_open',
                  'time_close', 'force_close')


class HistoryGuestSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = bk_models.HistoryGuest
        fields = ('id', 'guest_name', 'court', 'date_time',
                  'pay', 'guest_email', 'guest_tel', 'receipt')


class HistoryMemberSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = bk_models.HistoryMember
        fields = ('id', 'username', 'court', 'date_time',
                  'price_normal', 'total_ds', 'pay', 'state', 'receipt')


class HistoryGroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = bk_models.HistoryGroup
        fields = ('header', 'court', 'day', 'time')


class RequestMemberSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = bk_models.RequesMember
        fields = ('header', 'member', 'is_create', 'state')


class RefundSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = bk_models.Refund
        fields = ('history', 'detail', 'state')


class StatusSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = bk_models.Status
        fields = ('court', 'name', 'time')

# class PriceSerializer(serializers.HyperlinkedModelSerializer):
#     class Meta:
#         model = bk_models.Price
#         fields = ('court', 'price_normal', 'ds_mem',
#                   'ds_time', 'ds_gang', 'refund')


# class TimeSerializer(serializers.HyperlinkedModelSerializer):
#     class Meta:
#         model = bk_models.Time
#         fields = ('court', 'time_open', 'time_close',
#                   'ds_time_start', 'ds_time_end', 'refund_time_gap')


# class RefundSerializer(serializers.HyperlinkedModelSerializer):
#     class Meta:
#         model = bk_models.Refund
#         fields = ('history_member', 'time_stamp', 'state')
