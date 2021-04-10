# from django.views import View
# from member import models as mem_models
# from booking import models as bk_models
# from rest_framework import viewsets  # for monitor api
# from . import serializers as s  # for monitor api

# # Create your views here.


# class GroupViewSet(viewsets.ModelViewSet):
#     queryset = mem_models.Group.objects.all().order_by('id')
#     serializer_class = s.GroupSerializer


# class GroupMemberViewSet(viewsets.ModelViewSet):
#     queryset = mem_models.GroupMember.objects.all().order_by('id')
#     serializer_class = s.GroupMemberSerializer


# class MemberViewSet(viewsets.ModelViewSet):
#     queryset = mem_models.Member.objects.all().order_by('id')
#     serializer_class = s.MemberSerializer


# class RequestMemberViewSet(viewsets.ModelViewSet):
#     queryset = mem_models.Request.objects.all().order_by('id')
#     serializer_class = s.RequestMemberSerializer


# class RequestViewSet(viewsets.ModelViewSet):
#     queryset = mem_models.Request.objects.all().order_by('id')
#     serializer_class = s.RequestSerializer


# class CheckPaymentViewSet(viewsets.ModelViewSet):
#     queryset = bk_models.CheckPayment.objects.all().order_by('id')
#     serializer_class = s.CheckPaymentSerializer


# class CourtDetailViewSet(viewsets.ModelViewSet):
#     queryset = bk_models.CourtDetail.objects.all().order_by('id')
#     serializer_class = s.CourtDetailSerializer


# class OtherDetailViewSet(viewsets.ModelViewSet):
#     queryset = bk_models.OtherDetail.objects.all().order_by('id')
#     serializer_class = s.OtherDetailSerializer


# class HistoryGuestViewSet(viewsets.ModelViewSet):
#     queryset = bk_models.HistoryGuest.objects.all().order_by('id')
#     serializer_class = s.HistoryGuestSerializer


# class HistoryMemberViewSet(viewsets.ModelViewSet):
#     queryset = bk_models.HistoryMember.objects.all().order_by('id')
#     serializer_class = s.HistoryMemberSerializer


# class HistoryGroupViewSet(viewsets.ModelViewSet):
#     queryset = bk_models.HistoryGroup.objects.all().order_by('id')
#     serializer_class = s.HistoryGroupSerializer


# class RefundViewSet(viewsets.ModelViewSet):
#     queryset = bk_models.Refund.objects.all().order_by('id')
#     serializer_class = s.RefundSerializer


# class StatusViewSet(viewsets.ModelViewSet):
#     queryset = bk_models.Status.objects.all().order_by('id')
#     serializer_class = s.StatusSerializer


# # class RefundViewSet(viewsets.ModelViewSet):
# #     queryset = bk_models.Refund.objects.all().order_by('id')
# #     serializer_class = s.RefundSerializer


# # class PriceViewSet(viewsets.ModelViewSet):
# #     queryset = bk_models.Price.objects.all().order_by('id')
# #     serializer_class = s.PriceSerializer


# # class TimeViewSet(viewsets.ModelViewSet):
# #     queryset = bk_models.Time.objects.all().order_by('id')
# #     serializer_class = s.TimeSerializer
