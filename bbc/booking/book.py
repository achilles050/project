from . import models
from member.models import Member
from datetime import time
from django.core.mail import send_mail


def check_valid(court, yourtime):
    try:
        t = time(yourtime)
        print('yourtime : ', t)
        detail = models.OtherDetail.objects.get(pk=1)
        print('open : ', detail.time_open)
        print('close : ', detail.time_close)

        if t >= detail.time_open and t <= detail.time_close:
            print('OPEN!!!')
        else:
            print('CLOSE!!!')
            return False

        q = models.Status.objects.filter(time=t).filter(court=court)
        print(q[0].name)
        print('NOT AVAILABLE', models.Status.objects.filter(
            time=t).filter(court=court))
        return False

    except Exception as e:
        print('Error is : ', e)
        print('AVAILABLE')
        return True


def booking(member, court, yourtime):
    try:
        t = time(int(yourtime))
        print(member)
        print(t)
        book = models.HistoryMember(member=Member.objects.get(username=member), court=models.CourtDetail.objects.get(
            court_number=court), time=t) #state default = 0 >>> booking
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
