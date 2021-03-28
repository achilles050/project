from . import models


def group_mem_per(memberid, groupid):
    print(memberid)
    print(groupid)
    q = models.GroupMember.objects.filter(
        group=groupid).filter(member=memberid).exists()
    return q  # .values()


def group_head_per(memberid, groupid):
    print(memberid)
    print(groupid)
    q = models.Group.objects.filter(header=memberid).exists()
    return q
