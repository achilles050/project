from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Group(models.Model):
    class Meta:
        db_table = 'group'
    group = models.CharField(max_length=100, unique=True)
    header = models.ForeignKey(
        'Member', on_delete=models.CASCADE)
    outside_detail = models.CharField(max_length=500)
    inside_detail = models.CharField(max_length=500)
    # change when pay to next month court to True(use cronjob check this change below)
    is_continue = models.BooleanField(default=False)
    # change when not pay next month(use cronjob to change) False = not use now(not show in list group)
    is_active = models.BooleanField(default=False)


class GroupMember(models.Model):
    class Meta:
        db_table = 'group_member'
    group = models.ForeignKey(
        Group, on_delete=models.CASCADE)
    member = models.ForeignKey(
        'Member', on_delete=models.CASCADE)
    on_court = models.BooleanField(default=False)
    # # for show role in group h = header, m = member, j = join, q = quite
    # role = models.CharField(max_length=1, default='m')


class Member(User):
    class Meta:
        db_table = 'member'
    tel = models.CharField(max_length=10)
    birthday = models.DateField(null=True)
    gender = models.CharField(max_length=10)
    mygroup = models.ForeignKey(
        Group, on_delete=models.SET_NULL, null=True)
    # 0 = member, 1 = header, 2 = creating(header), 3 = joining(member who join group)
    group_role = models.IntegerField(null=True)

    def __str__(self):
        return self.username


class RequestMember(models.Model):  # for create, join, change header notification
    class Meta:
        db_table = 'request_member'
    header = models.ForeignKey(Group, on_delete=models.CASCADE)
    member = models.ForeignKey(Member, on_delete=models.CASCADE)
    # when request to create group = 0, join = 1, change header = 2
    action = models.IntegerField(default=None)
    # change to True when action that request
    state = models.BooleanField(default=False)
