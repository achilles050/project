from . import models
# from django.db.models import Q


def group_mem_per(memberid, groupid):
    q_m = models.GroupMember.objects.filter(
        group_id=groupid).filter(member_id=memberid).filter(role='m').exists()
    q_h = models.GroupMember.objects.filter(
        group_id=groupid).filter(member_id=memberid).filter(role='h').exists()
    return q_m or q_h


def group_head_per(memberid, groupid):
    q = models.GroupMember.objects.filter(
        group_id=groupid).filter(member_id=memberid).filter(role='h').exists()
    return q
