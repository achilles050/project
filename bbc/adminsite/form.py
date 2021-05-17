from django import forms
from django.utils import timezone
from booking.models import AllCourtInfo, EachCourtInfo
from member.models import Member
from datetime import timedelta, time, datetime
from booking import models as booking_models


def time_range():
    info = booking_models.AllCourtInfo.objects.all()[0]
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

    return time_range


def time_choices():
    info = booking_models.AllCourtInfo.objects.all()[0]
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
    data = list()
    for t in time_range:
        data.append((str(t)+':00:00', str(t)+':00'))
    return data


def time_choices2():
    info = booking_models.AllCourtInfo.objects.all()[0]
    if info.open_time.hour > info.close_time.hour:
        time_range = list(
            range((info.close_time.hour+1), (info.open_time.hour+1)))
        l = list(range(1, 25))
        for value in time_range:
            if value in l:
                l.remove(value)
        time_range = l
    else:
        time_range = list(range(info.open_time.hour, info.close_time.hour))
    data = list()
    for t in time_range:
        data.append((str(t)+':00:00', str(t)+':00'))
    return data


def court_choices():
    court_number = booking_models.EachCourtInfo.objects.values_list(
        "court_number", flat=True).order_by('court_number')
    data = list()
    for c in court_number:
        data.append((c, 'Court '+str(c)))
    return data


def date_choice():
    info = booking_models.AllCourtInfo.objects.all()[0]
    numdays = info.range_booking.days
    dateList = []
    for x in range(0, numdays):
        dateList.append(datetime.now().date() + timedelta(days=x))
    date_choice_list = []
    for value in dateList:
        date_choice_list.append((value, value.isoformat()))
    return date_choice_list


class AllCourtForm(forms.ModelForm):
    class Meta:
        model = AllCourtInfo
        fields = ('__all__')
        # requireds = {
        #     'force_close': True,
        # }
        widgets = {
            'open_time': forms.TimeInput(format='%H:%M'),
            'close_time': forms.TimeInput(format='%H:%M'),
            'announce': forms.Textarea(),
            'contacts': forms.Textarea(),
            'rules': forms.Textarea(),

        }
        labels = {
            'num_of_creategroup': 'Number of create group',
            'announce': 'Announce',
            'contacts': 'Contacts',
            'rules': 'Rules'
        }

    range_booking = forms.ChoiceField(
        choices=[
            (timedelta(days=1), "1 day"),
            (timedelta(days=3), "3 days"),
            (timedelta(days=7), "7 days"),
        ],
        label='Range personal booking'
    )

    payment_member_duration = forms.ChoiceField(
        choices=[
            (timedelta(minutes=1), "1 min"),
            (timedelta(minutes=3), "3 mins"),
            (timedelta(minutes=5), "5 mins"),
            (timedelta(minutes=10), "10 mins"),
            (timedelta(minutes=30), "30 mins"),
            (timedelta(hours=1), "1 hour"),
        ],
        label='Payment after booking for member'
    )

    payment_guest_duration = forms.ChoiceField(
        choices=[
            (timedelta(minutes=1), "1 min"),
            (timedelta(minutes=3), "3 mins"),
            (timedelta(minutes=5), "5 mins"),
            (timedelta(minutes=10), "10 mins"),
            (timedelta(minutes=30), "30 mins"),
            (timedelta(hours=1), "1 hour"),
        ],
        label='Payment after booking for guest'
    )

    payment_group_duration = forms.ChoiceField(
        choices=[
            (timedelta(minutes=1), "1 min"),
            (timedelta(minutes=3), "3 mins"),
            (timedelta(minutes=5), "5 mins"),
            (timedelta(minutes=10), "10 mins"),
            (timedelta(minutes=30), "30 mins"),
            (timedelta(hours=1), "1 hour"),
        ],
        label='Payment after booking for group'
    )

    refund_member_duration = forms.ChoiceField(
        choices=[
            (timedelta(days=1), "1 day"),
            (timedelta(days=3), "3 days"),
            (timedelta(days=7), "7 days"),
        ],
        label='Refund before ... for member'
    )


class EachCourtForm(forms.ModelForm):
    class Meta:
        model = EachCourtInfo
        fields = ['court_number', 'price_normal', 'price_ds_mem', 'price_ds_group',
                  'price_ds_time', 'time_ds_start', 'time_ds_end', 'is_maintain']
        widgets = {
            'time_ds_start': forms.TimeInput(format='%H:%M'),
            'time_ds_end': forms.TimeInput(format='%H:%M'),
        }


class BookingForm(forms.Form):
    # date = forms.DateField(widget=forms.SelectDateWidget(
    #     empty_label=("Choose Year", "Choose Month", "Choose Day")))
    date = forms.ChoiceField(choices=date_choice())
    from_time = forms.ChoiceField(choices=time_choices)
    to_time = forms.ChoiceField(choices=time_choices2)
    court = forms.ChoiceField(choices=court_choices)
    name = forms.CharField()
    tel = forms.CharField()
    email = forms.EmailField()


class MemberForm(forms.ModelForm):

    this_year = datetime.now().year

    class Meta:
        model = Member
        fields = ('username', 'first_name', 'last_name', 'email',
                  'is_active', 'tel', 'birthday', 'gender', 'public', 'virtualid')
        widgets = {
            'birthday': forms.SelectDateWidget(years=range(datetime.now().year-100, datetime.now().year+1))
        }


class CheckPaymentForm(forms.ModelForm):
    class Meta:
        model = booking_models.Payment
        fields = ('__all__')
