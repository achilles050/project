from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Group(models.Model):
    class Meta:
        db_table = 'bbc_group'
    group_name = models.CharField(max_length=100, unique=True)
    outside_detail = models.CharField(max_length=500)
    inside_detail = models.CharField(max_length=500)
    # change when pay to next month court to True(use cronjob check this change below)
    is_continue = models.BooleanField(default=False)
    # change when not pay next month(use cronjob to change) False = not use now(not show in list group)
    is_active = models.BooleanField(default=False)
    # count are count when member accept creste group request
    count = models.IntegerField(default=0)


class GroupMember(models.Model):
    class Meta:
        db_table = 'bbc_groupmember'
    group = models.ForeignKey(
        Group, on_delete=models.CASCADE, null=True, related_name='group')
    member = models.ForeignKey(
        'Member', on_delete=models.CASCADE)
    # for show role in group h = header, m = member, j=join
    role = models.CharField(max_length=1, default='')
    on_court = models.BooleanField(default=False)


class Member(User):
    class Meta:
        db_table = 'bbc_member'
    tel = models.CharField(max_length=10)
    birthday = models.DateField(null=True)
    gender = models.CharField(max_length=10)
    # for show in creategroup request
    public = models.BooleanField(default=True)


class Request(models.Model):

    class Meta:
        db_table = 'bbc_request'
    group = models.ForeignKey(Group, on_delete=models.CASCADE, null=True)
    sender = models.ForeignKey(
        Member, on_delete=models.CASCADE, to_field='username', related_name='sender')
    receiver = models.ForeignKey(
        Member, on_delete=models.CASCADE, to_field='username', related_name='receiver')
    # when request to create group = 0, join = 1, change header = 2
    action = models.IntegerField(default=None)
    # change to True when action that request
    read = models.BooleanField(default=False)
