from django import forms
from booking.models import AllCourtInfo


class AllCourtForm(forms.ModelForm):
    class Meta:
        model = AllCourtInfo
        fields = ['force_close']

    force_close = forms.BooleanField()
    range_booking = forms.DurationField()
