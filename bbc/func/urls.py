from django.urls import include, path
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register(r'Group', views.GroupViewSet)
router.register(r'GroupMember', views.GroupMemberViewSet)
router.register(r'Member', views.MemberViewSet)
router.register(r'RequestMember', views.RequestMemberViewSet)
router.register(r'Request', views.RequestViewSet)

router.register(r'CheckPayment', views.CheckPaymentViewSet)
router.register(r'CourtDetail', views.CourtDetailViewSet)
router.register(r'OtherDetail', views.OtherDetailViewSet)
router.register(r'HistoryGuest', views.HistoryGuestViewSet)
router.register(r'HistoryMember', views.HistoryMemberViewSet)
router.register(r'HistoryGroup', views.HistoryGroupViewSet)
router.register(r'Refund', views.RefundViewSet)
router.register(r'Status', views.StatusViewSet)
# router.register(r'Price', views.PriceViewSet)
# router.register(r'Time', views.TimeViewSet)
# router.register(r'Refund', views.RefundViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
    path('api-auth/', include('rest_framework.urls')),
]
