from . import models
from member.models import Member
from datetime import time, datetime  # , timedelta
from django.core.mail import send_mail

# +timedelta(hours=1)


def check_valid(court, yourtime):  # time in hour unit
    try:
        t = time(yourtime)
        detail = models.OtherDetail.objects.get(pk=1)
        maintain = models.CourtDetail.objects.get(
            court_number=court).maintain
        past = yourtime >= datetime.now().hour
        valid = not models.Status.objects.filter(
            time=t).filter(court_id__court_number=court).filter(time_out__gt=datetime.now().time()).exists()
        if yourtime in range(detail.time_open.hour, detail.time_close.hour) and valid and not maintain and past:
            return True
        else:
            return False

    except Exception as e:
        print('Error is : ', e)
        return None


def court():
    try:
        # number = models.CourtDetail.objects.all()
        number = models.CourtDetail.objects.values("court_number")
        print(type(number))
        # print(number.count())
        print(number)
        court = list()
        # court.append({}) for i in
        print('\n')

        time = models.OtherDetail.objects.values("time_open", "time_close")
        print(time)
        print(type(time[0]['time_open']))
        print(time[0]['time_open'])
        # print(time_open[0]["time_open"].hour)
        # print('%02d' % time_open[0]["time_open"].hour)
        for i in number:
            print(type(i["court_number"]), ' ', i["court_number"])
            print('%02d' % i["court_number"])

    except Exception as e:
        print(f'Error !!! {e}')


def booking(member, court, yourtime):
    try:
        t = time(int(yourtime))
        print(member)
        print(t)
        book = models.HistoryMember.objects.create(member=Member.objects.get(username=member), court=models.CourtDetail.objects.get(
            court_number=court), time=t)  # state default = 0 >>> booking
        book.save()
        print('ok')
        return True
    except Exception as e:
        print('error :', e)
        return False


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
