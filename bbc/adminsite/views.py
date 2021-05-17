from django.shortcuts import render
from django.http import HttpResponse
from django.http.response import JsonResponse
from django.views.generic import CreateView, DetailView, UpdateView, ListView, View
from django.utils import timezone

from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import permission_required

from uuid import uuid4
from datetime import timedelta, datetime, time, date

from . import form
from booking import models as booking_models
from booking import book
from booking.views import Booking as booking_status
from member import models as member_models

# Create your views here.


# @staff_member_required
# @permission_required('is_staff')  # , login_url='/login/')
class AdminHome(PermissionRequiredMixin, View):
    permission_required = 'is_staff'

    def get(self, request):
        return render(request, 'adminsite/home.html')


class SettingHome(PermissionRequiredMixin, View):
    permission_required = 'is_staff'

    def get(self, request):
        court_number = booking_models.EachCourtInfo.objects.values_list(
            "court_number", flat=True).order_by('court_number')
        return render(request, 'adminsite/setting_home.html', {'court_number': court_number})


class AllCourtSetting(PermissionRequiredMixin, View):
    permission_required = 'is_staff'

    def get(self, request):
        query_obj = booking_models.AllCourtInfo.objects.values().all()[0]
        myform = form.AllCourtForm(query_obj)
        return render(request, 'adminsite/setting_allcourt.html', {'form': myform})

    def post(self, request):
        query_obj = booking_models.AllCourtInfo.objects.all()[0]
        myform = form.AllCourtForm(request.POST, instance=query_obj)

        if myform.is_valid():
            myform.save(commit=True)
        return render(request, 'adminsite/setting_allcourt.html', {'form': myform})


class EachCourtSetting(PermissionRequiredMixin, UpdateView):
    permission_required = 'is_staff'

    form_class = form.EachCourtForm
    model = booking_models.EachCourtInfo
    template_name = 'adminsite/setting_eachcourt.html'
    slug_field = 'court_number'
    slug_url_kwarg = 'court_number'
    success_url = '/adminsite/setting/'


class AdminBooking(PermissionRequiredMixin, View):
    permission_required = 'is_staff'

    def get(self, request):
        dt_now = datetime.now()
        mydate = dt_now.date()
        from_time = time(dt_now.hour)
        to_time = time(dt_now.hour+1)
        data = {'date': mydate, 'from_time': from_time,
                'to_time': to_time}
        myform = form.BookingForm(initial=data)
        return render(request, 'adminsite/booking.html', {'form': myform})

    def post(self, request):
        data = request.POST
        myform = form.BookingForm(data)

        if myform.is_valid():
            booking_obj_list = list()
            all_price_normal = 0
            all_ds_time = 0
            all_ds_mem = 0
            from_time = data['from_time']
            to_time = data['to_time']
            str_date = data['date']
            court = data['court']
            name = data['name']
            tel = data['tel']
            email = data['email']

            q_allcourtinfo = booking_models.AllCourtInfo.objects.all()[0]

            dt_now = timezone.make_aware(datetime.now())
            exp = q_allcourtinfo.payment_member_duration
            dt_exp = dt_now + exp

            # from_time = datetime.strptime(from_time, '%H:%M:%S').hour
            # to_time = datetime.strptime(to_time, '%H:%M:%S').hour
            from_time = int(from_time[:2])
            to_time = int(to_time[:2])
            booking_date = datetime.strptime(str_date, '%Y-%m-%d').date()
            booking_time = []
            for mytime in range(from_time, to_time):
                if mytime in form.time_range():
                    booking_time.append(mytime)

            for mytime in booking_time:
                if book.check_valid(court=court, mytime=mytime, mydate=booking_date):
                    booking_datetime = timezone.make_aware(
                        datetime.combine(booking_date, time(mytime)))
                    q_court = booking_models.EachCourtInfo.objects.get(
                        court_number=court)
                    price_normal = q_court.price_normal
                    ds_mem = 0
                    ds_time = q_court.price_ds_time
                    ds_time_start = q_court.time_ds_start.hour
                    ds_time_end = q_court.time_ds_end.hour

                    if not mytime in range(int(ds_time_start), int(ds_time_end)):
                        ds_time = 0

                    while True:
                        bookingid = uuid4().hex
                        if booking_models.Booking.objects.filter(bookingid=bookingid).exists():
                            pass
                        else:
                            break

                    booking_obj, booking_created = booking_models.Booking.objects.get_or_create(
                        name=name,
                        email=email,
                        tel=tel,
                        member=None,
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
                else:
                    break

            if len(booking_time) != len(booking_obj_list):
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

        return render(request, 'adminsite/booking.html', {'form': myform})


class ListMember(ListView):
    model = member_models.Member
    template_name = 'adminsite/member.html'

    def get_queryset(self):
        member = member_models.Member.objects.filter(
            is_staff=False)  # .filter(is_active=True)
        return member


class DetailMember(PermissionRequiredMixin, UpdateView):
    permission_required = 'is_staff'

    form_class = form.MemberForm
    model = member_models.Member
    template_name = 'adminsite/member_detail.html'
    success_url = '/adminsite/member/'


class Status(PermissionRequiredMixin, View):
    permission_required = 'is_staff'

    def get(self, request):
        myform = form.StatusForm
        return render(request, 'adminsite/status.html', {'form': myform})

    def post(self, request):
        return StatusDetail().get(request)


class StatusDetail(PermissionRequiredMixin, View):
    permission_required = 'is_staff'

    def get(self, request):
        date = request.POST
        if not request.GET._mutable:
            request.GET._mutable = True

        print(date)
        date = date['date_year'] + \
            '%02d' % int(date['date_month'])+'%02d' % int(date['date_day'])

        request.GET['d'] = date
        data = booking_status().get(request)
        print(data.content)
        myform = form.StatusForm
        return render(request, 'adminsite/status.html', {'form': myform})
