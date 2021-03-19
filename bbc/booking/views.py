import json
from datetime import datetime, time, timedelta
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
        else:
            data = dict({'data': 'close'})

        q_courtdetail = models.CourtDetail.objects.all()
        s_courtdetail = serializers.CourtDetailSerializer(
            q_courtdetail, many=True)
        data['court_detail'] = s_courtdetail.data

        return JsonResponse(data)

    def post(self, request):  # book court
        court = int(request.data['court'])
        yourtime = int(request.data['time'])
        now = datetime.now()
        dt_booked = datetime.combine(now.date(), time(yourtime))
        duration_tm = 10 if request.user.id is not None else 1
        time_out = (now + timedelta(minutes=duration_tm)).time()
        name = request.user.first_name if request.user.id is not None else 'guest'

        if request.user.id is None:
            guest_email = 'guest@email.com'
            guest_tel = '0800000000'

        if book.check_valid(court=court, yourtime=yourtime):
            q_court = models.CourtDetail.objects.get(court_number=court)
            pay = q_court.price_normal
            dis_mem = q_court.price_ds_mem
            dis_time = q_court.price_ds_time
            dis_time_start = q_court.time_ds_start.hour
            dis_time_end = q_court.time_ds_end.hour

            status_obj, status_created = models.Status.objects.get_or_create(
                court=q_court, name=name, time=time(yourtime),
                time_out=time_out)

            if request.user.id is not None:
                q_member = models.Member.objects.get(username=request.user)
                if not yourtime in range(dis_time_start, dis_time_end):
                    dis_time = 0

                history_obj, history_create = model.HistoryMember.objects.get_or_create(
                    username=q_member, court=q_court, price_normal=normal_price,
                    total_ds=dis_time+dis_mem, pay=pay-dis_time-dis_mem,
                    date_time=datetime.combine(now.date(), time(yourtime)),
                    receipt=uuid4().hex)
            else:
                history_obj, history_create = models.HistoryGuest.objects.get_or_create(
                    guest_name=name, court=q_court,
                    date_time=datetime.combine(now.date(), time(yourtime)),
                    pay=pay, guest_email=guest_email, guest_tel=guest_tel,
                    receipt=uuid4().hex)

            if status_created and history_create:
                status_obj.receipt = history_obj.receipt
                status_obj.save()
                return JsonResponse({'success': True, 'receipt': history_obj.receipt})
            else:
                status_obj.delete() if status_created else history_obj.delete()

        return JsonResponse({'success': False})


class confirm(APIView):
    def post(self, request):
        receipt = request.data['receipt']

        if models.HistoryMember.objects.filter(receipt=receipt).exists():
            q_history = models.HistoryMember.objects.get(receipt=receipt)

        elif models.HistoryGuest.objects.filter(receipt=receipt).exists():
            q_history = models.HistoryGuest.objects.get(receipt=receipt)
        else:
            print('receipt error')
            return JsonResponse({'message': 'error receipt nbt found'})

        q_history.state = 1
        q_history.save()
        return JsonResponse({'message': 'confirm success'})
