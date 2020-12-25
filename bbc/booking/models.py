from django.db import models
from member.models import Member, Group
from django.contrib.auth.models import User
# Create your models here.


class CheckPayment(models.Model):
    class Meta:
        db_table = 'check_payment'
    history_guest = models.ForeignKey(
        'HistoryGuest', on_delete=models.CASCADE, null=True)
    history_member = models.ForeignKey(
        'HistoryMember', on_delete=models.CASCADE, null=True)
    history_group = models.ForeignKey(
        'HistoryGroup', on_delete=models.CASCADE, null=True)
    transection = models.DecimalField(max_digits=20, decimal_places=0)
    #ref2 = models.DecimalField(max_digits=20, decimal_places=0)
    amount = models.DecimalField(max_digits=5, decimal_places=2)
    # change when check success by admin
    state = models.BooleanField(default=False)
    # changee when checking found transaction if not change state in hsmem to 3
    is_found = models.BooleanField(default=False)


class CourtDetail(models.Model):
    class Meta:
        db_table = 'court_detail'
    court_number = models.IntegerField(unique=True)
    price_normal = models.DecimalField(max_digits=5, decimal_places=2)
    price_ds_mem = models.DecimalField(max_digits=5, decimal_places=2)
    price_ds_gang = models.DecimalField(max_digits=5, decimal_places=2)
    price_ds_time = models.DecimalField(max_digits=5, decimal_places=2)
    time_ds_start = models.TimeField()
    time_ds_end = models.TimeField()
    maintain = models.BooleanField(default=False)


class OtherDetail(models.Model):
    class Meta:
        db_table = 'other_detail'
    refund_gap_minute = models.DecimalField(max_digits=3, decimal_places=0)
    confirm_gap_minute = models.DecimalField(max_digits=3, decimal_places=0)
    refund_percent = models.DecimalField(max_digits=3, decimal_places=0)
    time_open = models.TimeField()
    time_close = models.TimeField()
    force_close = models.BooleanField(default=False)
    #annouce = models.CharField(max_length=500)


class HistoryGuest(models.Model):
    class Meta:
        db_table = 'history_guest'
    guest_name = models.CharField(max_length=50)
    court = models.ForeignKey(
        CourtDetail, on_delete=models.CASCADE, to_field='court_number')
    date_time = models.DateTimeField()
    pay = models.DecimalField(max_digits=5, decimal_places=2, null=True)
    guest_email = models.EmailField()
    guest_tel = models.CharField(max_length=10)
    receipt = models.CharField(max_length=32, null=True)
    timestamp = models.DateTimeField(auto_now=True)


class HistoryMember(models.Model):
    class Meta:
        db_table = 'history_member'
    username = models.ForeignKey(
        Member, on_delete=models.CASCADE)
    court = models.ForeignKey(
        CourtDetail, on_delete=models.CASCADE, to_field='court_number')
    date_time = models.DateTimeField()
    price_normal = models.DecimalField(
        max_digits=5, decimal_places=2, null=True)
    total_ds = models.DecimalField(max_digits=5, decimal_places=2, null=True)
    pay = models.DecimalField(max_digits=5, decimal_places=2, null=True)
    # 0 = booking, 1 = confirmed, 2 = canceled, 3 = checkedPayment false(checking not found transaction)
    state = models.IntegerField(default=0)
    receipt = models.CharField(max_length=32, null=True)
    timestamp = models.DateTimeField(auto_now=True)


class HistoryGroup(models.Model):
    class Meta:
        db_table = 'history_group'
    header = models.ForeignKey(
        Group, on_delete=models.CASCADE)
    court = models.ForeignKey(
        CourtDetail, on_delete=models.CASCADE, to_field='court_number')
    day = models.DecimalField(max_digits=1, decimal_places=0)
    time = models.TimeField()
    price_normal = models.DecimalField(
        max_digits=5, decimal_places=2, null=True)
    total_ds = models.DecimalField(max_digits=5, decimal_places=2, null=True)
    pay = models.DecimalField(max_digits=5, decimal_places=2, null=True)
    # 0 = booking, 1 = confirmed, 2 = canceled, 3 = checkedPayment false(checking not found transaction)
    state = models.IntegerField(default=0)
    receipt = models.CharField(max_length=32, null=True)
    timestamp = models.DateTimeField(auto_now=True)


class Refund(models.Model):
    class Meta:
        db_table = 'refund'
    history = models.ForeignKey(
        HistoryMember, on_delete=models.CASCADE)
    detail = models.CharField(max_length=20)
    # change when refund success by admin
    state = models.BooleanField(default=False)


class Status(models.Model):
    class Meta:
        db_table = 'status'
    court = models.ForeignKey(
        CourtDetail, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    time = models.TimeField()

    def __str__(self):
        mystr = self.court+' '+self.name+' '+self.time+'\n'
        return mystr


# show in admin only to show refund require from booked page
# class Refund(models.Model):
#     class Meta:
#         db_table = 'refund'
#     history_member = models.ForeignKey(
#         HistoryMember, on_delete=models.CASCADE)
#     time_stamp = models.TimeField(auto_now_add=True)

#     state = models.BooleanField(default=False)


# class Price(models.Model):
#     class Meta:
#         db_table = 'price'
#     court = models.ForeignKey(Court, on_delete=models.CASCADE)
#     price_normal = models.DecimalField(max_digits=5, decimal_places=2)
#     ds_mem = models.DecimalField(max_digits=5, decimal_places=2)
#     ds_time = models.DecimalField(max_digits=5, decimal_places=2)
#     ds_gang = models.DecimalField(max_digits=5, decimal_places=2)


# class Time(models.Model):
#     class Meta:
#         db_table = 'time'
#     court = models.ForeignKey(Court, on_delete=models.CASCADE)
#     time_open = models.TimeField()
#     time_close = models.TimeField()
#     ds_time_start = models.TimeField()
#     ds_time_end = models.TimeField()
#     refund_time_gap = models.DecimalField(
#         max_digits=3, decimal_places=0)  # in minute
