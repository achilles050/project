from . import models
from member.models import Member
from datetime import time, datetime, date  # , timedelta
from django.core.mail import send_mail
from django.utils import timezone

# +timedelta(hours=1)


def AddMonths(dt, d, m=1):
    newmonth = (((dt.month - 1) + m) % 12) + 1
    newyear = int(dt.year + (((dt.month - 1) + m) / 12))
    return date(newyear, newmonth, d)


def check_valid(court, mytime, mydate):  # time in hour unit
    try:
        dt = timezone.make_aware(datetime.combine(mydate, time(mytime)))
        info = models.AllCourtInfo.objects.all()[0]
        maintain = models.EachCourtInfo.objects.get(
            court_number=court).is_maintain
        now = datetime.now()
        now_hour = timezone.make_aware(
            datetime.combine(now.date(), time(now.hour)))
        past = dt >= now_hour
        inrange = dt <= timezone.make_aware(
            datetime.now() + info.range_booking)
        valid = not models.Booking.objects.filter(
            booking_datetime=dt).filter(court_id__court_number=court).filter(exp_datetime__gt=timezone.make_aware(datetime.now())).exists()
        if info.open_time.hour > info.close_time.hour:
            time_range = list(
                range(info.close_time.hour, info.open_time.hour))
            l = list(range(0, 24))
            for value in time_range:
                if value in l:
                    l.remove(value)
            time_range = l
        else:
            time_range = list(range(info.open_time.hour, info.close_time.hour))
        if mytime in time_range and valid and not maintain and past and inrange:
            return True
        else:
            return False

    except Exception as e:
        print('Error is : ', e)
        return None


def check_valid_group(court, mytime, mydate):  # time in hour unit
    try:
        dt = timezone.make_aware(datetime.combine(mydate, time(mytime)))
        info = models.AllCourtInfo.objects.all()[0]
        maintain = models.EachCourtInfo.objects.get(
            court_number=court).is_maintain
        now = datetime.now()
        now_hour = timezone.make_aware(
            datetime.combine(now.date(), time(now.hour)))
        past = dt >= now_hour
        twomonth = AddMonths(now, 1, m=2)
        inrange = dt.date() < twomonth
        inrange_member = not dt <= timezone.make_aware(
            datetime.now() + info.range_booking)
        valid = not models.Booking.objects.filter(
            booking_datetime=dt).filter(court_id__court_number=court).filter(exp_datetime__gt=timezone.make_aware(datetime.now())).exists()
        if info.open_time.hour > info.close_time.hour:
            time_range = list(
                range(info.close_time.hour, info.open_time.hour))
            l = list(range(0, 24))
            for value in time_range:
                if value in l:
                    l.remove(value)
            time_range = l
        else:
            time_range = list(range(info.open_time.hour, info.close_time.hour))

        if mytime in time_range and valid and not maintain and past and inrange and inrange_member:
            return True
        else:
            return False

    except Exception as e:
        print('Error is : ', e)
        return None


def check_valid_group_history(court, mytime, mydate):
    try:
        dt = timezone.make_aware(datetime.combine(mydate, time(mytime)))
        valid = not models.Booking.objects.filter(booking_datetime=dt).filter(
            court_id__court_number=court).filter(payment_state=1).exclude(group=None).exists()
        return valid
    except:
        print('Error is : ', e)
        return None


def check_valid_group_history_for_booking(court, mydate, mytime, mygroup):
    try:
        dt = timezone.make_aware(datetime.combine(mydate, time(mytime)))
        valid = models.Booking.objects.filter(booking_datetime=dt).filter(
            court_id__court_number=court).filter(payment_state=1).filter(group=mygroup).exists()
        return valid
    except:
        print('Error is : ', e)
        return None

# def booking(member, court, yourtime):
#     try:
#         t = time(int(yourtime))
#         print(member)
#         print(t)
#         book = models.HistoryMember.objects.create(member=Member.objects.get(username=member), court=models.CourtDetail.objects.get(
#             court_number=court), time=t)  # state default = 0 >>> booking
#         book.save()
#         print('ok')
#         return True
#     except Exception as e:
#         print('error :', e)
#         return False


# def confirm(history):
#     try:
#         query = models.HistoryMember.objects.get(pk=history)
#         query.state = 1 # 0 = booking, 1 = confirmed, 2 = canceled, 3 = checkedPayment false(checking not found transaction)
#         query.court
#         status = models.Status(court=,name=,time=)
#         status.save()
#         return True
#     except Exception as e:
#         print(e)
#         return False


def refund_check(history_id):
    try:
        m = models.HistoryMember.objects.filter(
            id=history_id).filter(status=True)
        print('ok')
    except:
        print('error!!!')


# def sendemail():
#     send_mail(
#         subject='SubjectTest',  # Subject here
#         message='MessageTest',  # Here is the message.
#         from_email='@gmail.com',  # from@example.com
#         recipient_list=['thorn3579@gmail.com'],  # to@example.com
#         fail_silently=False,
#     )


def test():
    try:
        # sendemail()
        send_mail(
            subject='SubjectTest',  # Subject here
            message='MessageTest',  # Here is the message.
            from_email='bbctesting01@gmail.com',  # from@example.com
            recipient_list=['thorn3579@gmail.com'],  # to@example.com
            fail_silently=False,
        )
    except Exception as e:
        print(e)
