import json
from datetime import time, timedelta, date
from uuid import uuid4
import calendar

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


class CheckRange(APIView):
    def get(sself, request):
        try:
            q_allcourt = models.AllCourtInfo.objects.all()[0]
            range_booking = q_allcourt.range_booking
            dt_range = datetime.now() + range_booking
            date_range = timezone.make_aware(dt_range).date()
            return JsonResponse({'range': date_range}, status=200)
        except Exception as e:
            print(e)
            return JsonResponse({'msg': 'error'}, status=400)

    def post(self, request):
        try:
            y = request.data['year']
            m = request.data['month']
            d = request.data['day']
            info = models.AllCourtInfo.objects.all()[0]
            dt = datetime(year=int(y), month=int(m)+1, day=int(d))
            inrange_less = dt.date() <= timezone.make_aware(
                datetime.now() + info.range_booking).date()
            inrange_more = dt.date() >= timezone.make_aware(datetime.now()).date()
            if inrange_less and inrange_more:
                date = str(y)+str(int(m)+1)+str(d)
                return JsonResponse({'msg': True, 'date': date}, status=200)
            else:
                return JsonResponse({'msg': False}, status=404)
        except Exception as e:
            print(e)
            return JsonResponse({'msg': False}, status=404)


class Booking(APIView):
    def get(self, request):  # query status court
        if not models.AllCourtInfo.objects.all()[0].force_close:
            get_date = request.GET.get('d', None)
            if get_date is not None:
                strdate = str(get_date)
                mydate = datetime.strptime(strdate, '%Y%m%d').date()
            else:
                mydate = datetime.now().date()
            time_q = models.AllCourtInfo.objects.all()[0]
            time_open = time_q.open_time.hour
            time_close = time_q.close_time.hour
            time = range(0, 24)
            # if time_open > time_close:
            #     time = list(range(time_close, time_open))
            #     l = list(range(0, 24))
            #     for value in time:
            #         if value in l:
            #             l.remove(value)
            #     time = l
            # else:
            #     time = list(range(time_open, time_close))
            court_list = models.EachCourtInfo.objects.values_list(
                "court_number", flat=True)
            l = list()
            for i, t in enumerate(time):
                str_time = str('%02d:00' % t+'-'+'%02d:00' % (t+1))
                l.append({'time': str_time})
                for c in court_list:
                    str_court = 'Court'+str(c)
                    if book.check_valid(court=c, mytime=t, mydate=mydate):
                        l[i][str_court] = True
                    else:
                        l[i][str_court] = False
            data = dict({'date': mydate})
            data['status'] = l
            q_eachcourtinfo = models.EachCourtInfo.objects.all()
            s_eachcourtinfo = serializers.EachCourtInfoSerializer(
                q_eachcourtinfo, many=True)
            data['eachcourt_info'] = s_eachcourtinfo.data
            return JsonResponse(data)
        else:
            return JsonResponse({'status': 'close'})

    def post(self, request):  # book court
        booking = request.data['arr']
        booking_obj_list = list()
        all_price_normal = 0
        all_ds_time = 0
        all_ds_mem = 0

        q_allcourtinfo = models.AllCourtInfo.objects.all()[0]

        if request.user.id is not None:
            name = request.user.first_name
            email = request.user.email
            tel = mem_models.Member.objects.get(username=request.user).tel
            member = mem_models.Member.objects.get(username=request.user)
            exp = q_allcourtinfo.payment_member_duration
        else:
            name = request.data['name']
            email = request.data['email']
            tel = request.data['phone']
            member = None
            exp = q_allcourtinfo.payment_quest_duration

        strbooking_date = request.data['date']
        booking_date = datetime.strptime(strbooking_date, '%Y-%m-%d').date()

        dt_now = timezone.make_aware(datetime.now())
        dt_exp = dt_now + exp

        for value in booking:
            court = int(value['column'][5:])
            mytime = int(value['time'][:2])
            if book.check_valid(court=court, mytime=mytime, mydate=booking_date):
                booking_datetime = timezone.make_aware(
                    datetime.combine(booking_date, time(mytime)))
                bookingid = uuid4().hex
                q_court = models.EachCourtInfo.objects.get(court_number=court)
                price_normal = q_court.price_normal
                ds_mem = q_court.price_ds_mem if request.user.id is not None else 0
                ds_time = q_court.price_ds_time
                ds_time_start = q_court.time_ds_start.hour
                ds_time_end = q_court.time_ds_end.hour

                if not mytime in range(int(ds_time_start), int(ds_time_end)):
                    ds_time = 0

                booking_obj, booking_created = models.Booking.objects.get_or_create(
                    name=name,
                    email=email,
                    tel=tel,
                    member=member,
                    court=q_court,
                    booking_datetime=booking_datetime,
                    exp_datetime=dt_exp,
                    price_normal=price_normal,
                    price_ds=ds_mem+ds_time,
                    price_pay=price_normal-ds_mem-ds_time,
                    bookingid=bookingid)

                if booking_created:
                    booking_obj_list.append(booking_obj)
                    all_price_normal += price_normal
                    all_ds_mem += ds_mem
                    all_ds_time += ds_time
                else:
                    booking_obj.delete()
                    break
        if len(booking) != len(booking_obj_list):
            if len(booking_obj_list) != 0:
                for value in booking_obj_list:
                    value.delete()
            return JsonResponse({'success': False})
        else:
            response_dict = dict()
            response_dict['success'] = True
            response_dict['bookingid'] = [
                value.bookingid for value in booking_obj_list]
            response_dict['price'] = {}
            response_dict['price']['normal_price'] = all_price_normal
            response_dict['price']['discount_time'] = all_ds_time
            response_dict['price']['discount_member'] = all_ds_mem
            response_dict['price']['pay'] = all_price_normal - \
                all_ds_time-all_ds_mem
            return JsonResponse(response_dict)
        return HttpResponse('??????')


class GroupBooking(APIView):
    def get(self, request):
        if request.user.id is None:
            return JsonResponse({'msg': 'Pls login'})
        q_headergroupmember = mem_models.GroupMember.objects.filter(
            role='h').filter(member_id=request.user.id).exists()

        if q_headergroupmember:
            q_group = mem_models.Group.objects.get(
                group_id=q_headergroupmember.group_id)
        else:
            return JsonResponse({'msg': 'You re not header'}, status=400)

        if not models.AllCourtInfo.objects.all()[0].force_close:
            get_date = request.GET.get('d', None)
            if get_date is not None:
                dayofweek = int(get_date)
            else:
                dayofweek = 0

            dt_now = datetime.now()
            date_nm = book.AddMonths(dt_now, 1)
            day = calendar.monthcalendar(date_nm.year, date_nm.month)[
                2][dayofweek]
            mydate = date(date_nm.year, date_nm.month, day)
            strdayofweek = calendar.day_name[dayofweek]

            time_q = models.AllCourtInfo.objects.all()[0]
            time_open = time_q.open_time.hour
            time_close = time_q.close_time.hour
            time = range(0, 24)
            court_list = models.EachCourtInfo.objects.values_list(
                "court_number", flat=True)
            l = list()
            for i, t in enumerate(time):
                str_time = str('%02d:00' % t+'-'+'%02d:00' % (t+1))
                l.append({'time': str_time})
                for c in court_list:
                    str_court = 'Court'+str(c)
                    if book.check_valid_group(court=c, mytime=t, mydate=mydate):
                        l[i][str_court] = True
                    else:
                        l[i][str_court] = False
            strdate = str(mydate.year)+'-'+str(mydate.month)+'-'+strdayofweek
            data = dict({'date': strdate})
            data['status'] = l
            q_eachcourtinfo = models.EachCourtInfo.objects.all()
            s_eachcourtinfo = serializers.EachCourtInfo2Serializer(
                q_eachcourtinfo, many=True)
            data['eachcourt_info'] = s_eachcourtinfo.data
            # models.Booking.objects.filter(group=q_group).filter(booking_datetime__=)
            mydata = {'msg': 'ok'}
            return JsonResponse(data)
        else:
            return JsonResponse({'status': 'close'})

    def post(self, request):
        pass


class Payment(APIView):
    def get(self, request):
        q = models.Payment.objects.all()
        print(q)
        s = serializers.PaymentSerializer(q, many=True)
        print('pass')
        d = dict({'data': s.data})
        return JsonResponse(d)

    def post(self, request):
        all_bookingid = request.data['bookingid']
        otp = 1234  # request.data['otp']
        booking_obj_list = []
        pay = 0

        for bookingid in all_bookingid:
            now = timezone.make_aware(datetime.now())
            q_bookingid = models.Booking.objects.filter(
                exp_datetime__gt=now).filter(bookingid=bookingid).filter(payment_state=0).exists()

            if q_bookingid:
                q_booking = models.Booking.objects.get(bookingid=bookingid)
                pay += q_booking.price_pay
                booking_obj_list.append(q_booking)
            else:
                return JsonResponse({'message': 'error bookingid not available'}, status=404)

        payment_obj, payment_created = models.Payment.objects.get_or_create(
            paymentid=uuid4().hex,
            payment_otp=otp,
            pay=pay)

        if payment_created:
            for value in booking_obj_list:
                value.payment_state = 1
                value.paymentid = payment_obj.paymentid
                value.exp_datetime = value.booking_datetime + \
                    timedelta(hours=1)
                value.save()
            return JsonResponse({'message': 'confirm success'})
        else:
            return JsonResponse({'message': 'confirm unsuccess'}, status=400)


class CheckPrice(APIView):
    def post(self, request):
        all_bookingid = request.data['bookingid']
        booking_obj_list = []
        pay = 0

        for bookingid in all_bookingid:
            now = timezone.make_aware(datetime.now())
            q_bookingid = models.Booking.objects.filter(
                exp_datetime__gt=now).filter(bookingid=bookingid).filter(payment_state=0).exists()

            if q_bookingid:
                q_booking = models.Booking.objects.get(bookingid=bookingid)
                pay += q_booking.price_pay
                booking_obj_list.append(q_booking)
            else:
                return JsonResponse({'message': 'error bookingid not available'}, status=404)
        d = dict()
        d['Bookingid'] = all_bookingid
        d['price'] = pay
        return JsonResponse(d)


class HistoryPayment(APIView):
    def get(self, request):
        q = models.Payment.objects.all()
        print(q)
        s = serializers.PaymentSerializer(q, many=True)
        print('pass')
        d = dict({'data': s.data})
        return JsonResponse(d)
