import json
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from . import models
from member.models import Member
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user
from datetime import time
from . import book
# Create your views here.


# @login_required(login_url='/login/')
def court_status(request):
    query = models.Status.objects.all()
    mydict = list()
    for i in query:
        mydict.append({'court': i.court.court_number,
                       'name': i.name,
                       'time': i.time.hour
                       })
    return HttpResponse(json.dumps(mydict), content_type='application/json')


def booking(request):
    try:
        member = get_user(request)
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
        query = Member.objects.get(username=member)
        # booking in status models and historymember
    except Exception as e:
        if e == 'error':
            pass
            # booking in status models and historyguest
        print(e)
    return 0
