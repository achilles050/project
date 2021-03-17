import json
from datetime import datetime, time, timedelta

from . import models
from . import book

from member import models as mem_models
from . import serializers as b_s

from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user
from django.http.response import JsonResponse
from django.core import serializers
from django.forms.models import model_to_dict
from django.core.serializers.json import DjangoJSONEncoder

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

        return JsonResponse(data)

    def post(self, request):  # book court
        court = int(request.data['court'])
        yourtime = int(request.data['time'])
        name = 'guest'  # request.data['name']
        now = datetime.now()
        time_out = (now + timedelta(minutes=1)).time()

        if request.user.id is not None:
            name = request.user.first_name
            time_out = (now + timedelta(minutes=10)).time()

        if book.check_valid(court=court, yourtime=yourtime):
            obj, created = models.Status.objects.get_or_create(
                court=models.CourtDetail.objects.get(court_number=court),
                name=name, time=time(yourtime),
                time_out=time_out)
            if created:
                return JsonResponse({'success': True})

        return JsonResponse({'success': False})


def testcourt(request):
    d = dict()
    d['data'] = '4546'
    return JsonResponse(d)

    book.court(1)
    return HttpResponse('ok')


def mybooking(request):

    try:

        member = mem_models.Member.objects.get(pk=request.user.pk)
        # member = get_object_or_404(mem_models.Member, id=request.user.pk)
        print(type(member))
        print(member)
        state = False
        if request.method == 'POST':
            court = request.POST.get('court')
            yourtime = request.POST.get('time')
            if book.check_valid(court=int(court), yourtime=int(yourtime)):
                if book.booking(member=member, court=court, yourtime=yourtime):
                    print('booking success waiting for confirm(pay)')
                    state = True
        if state:
            return HttpResponse('success')
        else:
            return HttpResponse('Try Again!!!')

    except Exception as e:
        print(e)
        return HttpResponse('error!!!!')


def confirm(request):
    try:
        member = get_user(request)
        query = mem_models.Member.objects.get(username=member)
        # booking in status models and historymember
    except Exception as e:
        if e == 'error':
            pass
            # booking in status models and historyguest
        print(e)
    return 0
