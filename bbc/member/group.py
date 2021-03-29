from . import models
# from django.db.models import Q


def group_mem_per(memberid, groupid):
    q_gm = models.GroupMember.objects.filter(
        group_id=groupid).filter(member_id=memberid).filter(role='m').exists()
    q_g = models.Group.objects.filter(
        header=memberid).filter(id=groupid).exists()
    return q_gm or q_g


def group_head_per(memberid, groupid):
    q = models.Group.objects.filter(
        header=memberid).filter(id=groupid).exists()
    return q
