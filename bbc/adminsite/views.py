from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import CreateView, UpdateView, View

from . import form
from booking import models as booking_models

# Create your views here.


class AllCourtSetting(UpdateView):
    # form_class = form.AllCourtForm
    model = booking_models.AllCourtInfo
    template_name = 'adminsite/setting_allcourt.html'
    # exclude = None
    fields = ('__all__')
    # fields = ['force_close', 'range_booking']
    # def get(self):
    #     return
    success_url = '/adminsite/setting/allcourt/1'

# class AllCourtSetting(View):
#     def get(self, request):
#         return render(request, 'admin/setting_allcourt.html', {'form': form.AllCourtForm})


class EachCourtSetting(UpdateView):
    # form_class = form.AllCourtForm
    model = booking_models.EachCourtInfo
    template_name = 'adminsite/setting_eachcourt.html'
    # exclude = None
    fields = ('__all__')
    # fields = ['force_close', 'range_booking']
    # def get(self):
    #     return
    success_url = '/adminsite/setting/eachcourt/1'
