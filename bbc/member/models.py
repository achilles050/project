from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Group(models.Model):
    class Meta:
        db_table = 'group'
    group_name = models.CharField(max_length=100, unique=True)
    header = models.ForeignKey(
        'Member', on_delete=models.CASCADE)
    outside_detail = models.CharField(max_length=500)
    inside_detail = models.CharField(max_length=500)
    # change when pay to next month court to True(use cronjob check this change below)
    is_continue = models.BooleanField(default=False)
    # change when not pay next month(use cronjob to change)
    is_active = models.BooleanField(default=True)


class GroupMember(models.Model):
    class Meta:
        db_table = 'group_member'
    group = models.ForeignKey(
        Group, on_delete=models.CASCADE)
    member = models.ForeignKey(
        'Member', on_delete=models.CASCADE)
    on_court = models.BooleanField(default=False)


class Member(User):
    class Meta:
        db_table = 'member'
    tel = models.CharField(max_length=10)
    birthday = models.DateField(null=True)
    gender = models.CharField(max_length=10)
    group_name = models.ForeignKey(
        Group, on_delete=models.SET_NULL, null=True)


# class GroupMember(models.Model):
#     class Meta:
#         db_table = 'group_member'
#     group = models.ForeignKey(
#         Group, to_field='group_name', on_delete=models.CASCADE)
#     member = models.ForeignKey(
#         Member, to_field='username', on_delete=models.CASCADE)
#     on_court = models.BooleanField(default=False)
