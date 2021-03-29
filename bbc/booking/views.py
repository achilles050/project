import json
from datetime import time, timedelta
from uuid import uuid4

from . import models
from . import book

from member import models as mem_models
from . import serializers

from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user
from django.http.response import JsonResponse
# from django.core import serializers
from django.forms.models import model_to_dict
# from django.core.serializers.json import DjangoJSONEncoder
from django.utils import timezone
from django.utils.datetime_safe import datetime

from rest_framework.views import APIView
# Create your views here.


class booking(APIView):
    def get(self, request):  # query status court
        if not models.OtherDetail.objects.get(pk=1).force_close:
            status_q = models.Status.objects.all()
            time_q = models.OtherDetail.objects.get(pk=1)
            time_open = time_q.time_open.hour
            time_close = time_q.time_close.hour
            time = range(time_open, time_close)
            court_list = models.CourtDetail.objects.values_list(
                "court_number", flat=True)
            l = list()
            for i, t in enumerate(time):
                str_time = str('%02d:00' % t+'-'+'%02d:00' % (t+1))
                l.append({'time': str_time})
                for c in court_list:
                    str_court = 'Court'+str(c)
                    if book.check_valid(court=c, yourtime=t):
                        l[i][str_court] = True
                    else:
                        l[i][str_court] = False
            data = dict({'status': l})
            q_courtdetail = models.CourtDetail.objects.all()
            s_courtdetail = serializers.CourtDetailSerializer(
                q_courtdetail, many=True)
            data['court_detail'] = s_courtdetail.data
            return JsonResponse(data)
        else:
            return JsonResponse({'status': 'close'})

    def post(self, request):  # book court
        booking = request.data['arr']
        status_obj_list = []
        history_obj_list = []
        normal_price = 0
        ds_time = 0
        ds_mem = 0
        q_other = models.OtherDetail.objects.get(pk=1)
        guest_gap = q_other.confirm_gap_min_guest
        mem_gap = q_other.confirm_gap_min_member

        if request.user.id is None:
            # guest = request.data['guest']
            name = request.data['name']  # guest['name']
            guest_email = request.data['email']  # guest['email']
            guest_tel = request.data['phone']  # guest['tel']
            duration_minute = guest_gap
        else:
            duration_minute = mem_gap
            name = request.user.first_name

        now = datetime.now()
        date_now = datetime.now().date()
        time_out = timezone.make_aware(
            (now + timedelta(minutes=duration_minute))).time()

        for value in booking:
            court = int(value['column'][5:])
            yourtime = int(value['time'][:2])
            dt_booked = datetime.combine(date_now, time(yourtime))
            dt_booked = timezone.make_aware(dt_booked)
            receipt = uuid4().hex

            if book.check_valid(court=court, yourtime=yourtime):
                q_court = models.CourtDetail.objects.get(court_number=court)
                pay = q_court.price_normal
                dis_mem = q_court.price_ds_mem
                dis_time = q_court.price_ds_time
                dis_time_start = q_court.time_ds_start.hour
                dis_time_end = q_court.time_ds_end.hour

                status_obj, status_created = models.Status.objects.get_or_create(
                    court=q_court, name=name, time=time(yourtime),
                    time_out=time_out, receipt=receipt)

                if not yourtime in range(int(dis_time_start), int(dis_time_end)):
                    dis_time = 0

                if request.user.id is not None:
                    q_member = models.Member.objects.get(username=request.user)
                    history_obj, history_create = models.HistoryMember.objects.get_or_create(
                        username=q_member, court=q_court, price_normal=normal_price,
                        total_ds=dis_time+dis_mem, pay=pay-dis_time-dis_mem,
                        date_time=dt_booked, receipt=receipt)
                else:
                    dis_mem = 0
                    history_obj, history_create = models.HistoryGuest.objects.get_or_create(
                        guest_name=name, court=q_court,
                        date_time=dt_booked, pay=pay, guest_email=guest_email, guest_tel=guest_tel,
                        receipt=receipt)

                if status_created and history_create:
                    status_obj_list.append(status_obj)
                    history_obj_list.append(history_obj)
                    normal_price += pay
                    ds_mem += dis_mem
                    ds_time += dis_time
                else:
                    status_obj.delete() if status_created else history_obj.delete()

        if len(booking) != len(status_obj_list):  # != len(history_obj_list):
            if len(status_obj_list) != 0:
                for value in status_obj_list:
                    value.delete()
            if len(history_obj_list) != 0:
                for value in history_obj_list:
                    value.delete()
            return JsonResponse({'success': False})
        else:
            response_dict = dict()
            response_dict['success'] = True
            response_dict['receipt'] = [
                value.receipt for value in history_obj_list]
            response_dict['price'] = {}
            response_dict['price']['normal_price'] = normal_price
            response_dict['price']['discount_time'] = ds_time
            response_dict['price']['discount_member'] = ds_mem
            return JsonResponse(response_dict)
        return HttpResponse('??????')


class confirm(APIView):
    def post(self, request):
        all_receipt = request.data['receipt']
        history_obj_list = []
        status_obj_list = []
        time_out_list = []

        for receipt in all_receipt:
            now = timezone.make_aware(datetime.now())
            receipt_in_status = models.Status.objects.filter(
                time_out__gt=now).filter(receipt=receipt).exists()
            q_otherdetail = models.OtherDetail.objects.get(pk=1)
            time_close = q_otherdetail.time_close

            if models.HistoryMember.objects.filter(receipt=receipt).filter(state=0).exists() and receipt_in_status:
                q_history = models.HistoryMember.objects.get(receipt=receipt)
                q_status = models.Status.objects.get(receipt=receipt)
            elif models.HistoryGuest.objects.filter(receipt=receipt).filter(state=0).exists() and receipt_in_status:
                q_history = models.HistoryGuest.objects.get(receipt=receipt)
                q_status = models.Status.objects.get(receipt=receipt)
            else:
                if len(history_obj_list) != 0:
                    for index in range(len(history_obj_list)):
                        print(history_obj_list[index].state)
                        history_obj_list[index].state = 0
                        history_obj_list[index].save()
                        status_obj_list[index].time_out = time_out_list[index]
                        status_obj_list[index].save()

                return JsonResponse({'message': 'error receipt not found'})

            time_out_list.append(q_status.time_out)
            status_obj_list.append(q_status)
            history_obj_list.append(q_history)
            q_history.state = 1
            q_history.save()
            q_status.time_out = time_close
            q_status.save()

        return JsonResponse({'message': 'confirm success'})
