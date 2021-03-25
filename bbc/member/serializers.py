from rest_framework import serializers
from rest_framework.serializers import UUIDField
from . import models
from func import serializers as s


class MemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Member
        fields = ['username', 'first_name', 'last_name',
                  'email', 'tel', 'birthday', 'gender']


class CreateGroupMemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Member
        fields = ['id', 'username']


# class RequestSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = models.Request
#         fields = ('sender', 'action', 'state',
#                   'email', 'tel', 'birthday', 'gender', 'mygroup')


class GroupmemberSerializer(serializers.ModelSerializer):
    # group_name = serializers.SlugRelatedField(
    #     read_only=True, slug_field='header', allow_null=True)

    # group = serializers.SlugRelatedField(
    #     read_only=True, slug_field='header', allow_null=True)

    member = serializers.SlugRelatedField(
        read_only=True, slug_field='first_name', allow_null=True, many=True)

    class Meta:
        model = models.GroupMember
        fields = ['group_name', 'member', 'on_court']


class MygroupSerializer(serializers.ModelSerializer):
    header = serializers.SlugRelatedField(
        read_only=True, slug_field='first_name', allow_null=True)

    group = serializers.StringRelatedField(many=True, allow_null=True)
    # member = group
    member = GroupmemberSerializer(many=True, allow_null=True, read_only=True)

    class Meta:
        model = models.Group
        fields = ['group_name', 'header', 'inside_detail', 'group', 'member']


class ListgroupSerializer(serializers.ModelSerializer):
    header = serializers.SlugRelatedField(
        read_only=True, slug_field='first_name', allow_null=True)
    # group = MembergroupSerializer(many=True, read_only=True, allow_null=True)
    group = serializers.StringRelatedField(many=True, allow_null=True)
    member = group

    class Meta:
        model = models.Group
        fields = ['group_name', 'header',
                  'outside_detail', 'group', 'member']
