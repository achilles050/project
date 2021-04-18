from . import models
from booking import models as booking_models
from . import serializers as s
from .form import LoginForm
from . import token
from . import group

from datetime import date
import json
import urllib.parse

from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt  # csrf_clear
from django.contrib.auth import authenticate, login, logout, get_user
from django.http.response import JsonResponse

from django.views import View
from django.views.generic import ListView
from django.views.generic.detail import DetailView

from rest_framework.decorators import api_view
from rest_framework.parsers import JSONParser
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from django.shortcuts import get_object_or_404

# Create your views here.


@api_view(['GET', 'POST'])
def Index(request):
    print(f'Index {request.user}')
    try:
        models.Member.objects.get(username=request.user)
        return HttpResponse(f'hi user!!! {request.user}')
    except:
        return HttpResponse('hi guest!!!')


@api_view(['GET', 'POST', 'PUT'])
def Register(request):
    if request.method == 'POST':
        username = request.data['username']
        password = request.data['password']
        firstname = request.data['firstname']
        lastname = request.data['lastname']
        email = request.data['email']
        tel = '00000221'  # request.data['tel']
        birthday = '1999/03/15'  # request.data['birthday']
        gender = 'male'  # request.data['gender']

        try:
            if not models.Member.objects.filter(email=email).exists():
                b = birthday.split('/')
                birth = date(int(b[0]), int(b[1]), int(b[2]))
                print(birth)
                regis = models.Member.objects.create_user(
                    username=username, password=password, email=email)
                regis.first_name = firstname
                regis.last_name = lastname
                regis.tel = tel
                regis.birthday = birth
                regis.gender = gender
                # regis.is_active = False
                regis.save()
                print('Register Success')
                return HttpResponse("Register Success")
            else:
                return HttpResponse("Email does exists")

        except Exception as e:
            print('Error !!! >>> ', e)
            return HttpResponse('Register Error!!! ', e)

    else:
        return HttpResponse('Try Again!!!')


class Login(APIView):
    def get(self, request):
        return render(request, 'login.html', {'form': LoginForm})

    def post(self, request):
        username = request.data['username']
        password = request.data['password']
        auth = authenticate(username=username, password=password)
        if auth is not None:
            login(request, auth)
            return JsonResponse({'username': username}, status=200)
        else:
            return JsonResponse({'message': 'try again'}, status=404)


# @login_required(login_url='/login/')
def Logout(request):
    try:
        print('going to logout')
        logout(request)
        print('logouted')
        return JsonResponse({'msg': 'logout successfully'}, status=200)
        # return HttpResponse('ok logouted')
    except Exception as e:
        print(e)
        return JsonResponse({'msg': 'error'}, status=404)


def Test(request):
    try:
        user = get_object_or_404(models.Member, username='thorn')
        mytoken1 = token.account_activation_token.make_token(user)
        print(user)
        print(mytoken1)
        print(type(mytoken1))
        print(token.account_activation_token.check_token(user, mytoken1))

        mytoken2 = token.default_token_generator.make_token(user)
        print(user)
        print(mytoken2)
        print(type(mytoken2))
        print(token.default_token_generator.check_token(user, mytoken2))

        return HttpResponse('ok', status=200)
    except Exception as e:
        print(f'Error = {e}')
        return HttpResponse('error')


class Profile(APIView):
    def get(self, request):
        try:
            if request.user.id is not None:
                print(f'This is {request.user} profile')
                member = models.Member.objects.get(pk=request.user.id)
                mem_serializer = s.MemberSerializer(member)
                return JsonResponse(mem_serializer.data, safe=False)
            return JsonResponse({'message': 'Pls login. (GET)'})
        except Exception as e:
            print(f'Error {e}')
            return JsonResponse({'message': 'Error(GET)'}, safe=False)

    def put(self, request):
        try:
            if request.user.id is not None:
                member_obj = models.Member.objects.get(pk=request.user.id)
                mem_serializer = s.MemberSerializer(
                    member_obj, data=request.data)
                if mem_serializer.is_valid():
                    mem_serializer.save()
                    return JsonResponse(mem_serializer.data, safe=False)
                return JsonResponse({'message': 'NOT CHANGE (POST)'}, safe=False)
        except Exception as e:
            print(f'Error {e}')
            return JsonResponse({'message': 'Error(POST)'}, safe=False)


class Creategroup(APIView):
    def get(self, request):
        try:
            if request.user.id is None:
                return JsonResponse({'msg': 'Login before create group'})
            mem_q = models.Member.objects.filter(
                is_active=True).exclude(username=request.user)
            mem_s = s.CreateGroupMemberSerializer(mem_q, many=True)
            return JsonResponse(mem_s.data, safe=False)
        except Exception as e:
            print(f'Error = {e}')
            return JsonResponse({'msg': 'Error (GET)'})

    def post(self, request):
        q_allcourt = booking_models.AllCourtInfo.objects.all()[0]
        number_creategroup = q_allcourt.num_of_creategroup
        if request.user.id is None:
            return JsonResponse({'msg': 'Login before create group'})

        q_header = models.Member.objects.get(username=request.user)
        member = request.data['member']
        group_name = request.data['group_name']

        if group_name == '':
            return JsonResponse({'msg': f'pls fill your group name!!!'}, status=400)

        if len(member) != number_creategroup:
            return JsonResponse({'msg': f'Error create group with {number_creategroup} member!!!'}, status=400)

        for value in member:
            if models.Member.objects.filter(virtualid=value).exists():
                pass
            else:
                return JsonResponse({'message': f'Error this userid {value} not found'}, status=404)

        group_obj, create = models.Group.objects.get_or_create(
            group_name=group_name, is_active=False)

        if not create:
            return JsonResponse({'message': f'Error this group name {group_obj.group_name} exists '}, status=400)
        else:
            models.GroupMember.objects.get_or_create(
                group=group_obj, member=q_header, role='h')

        for value in member:
            virtualid = value
            q_receiver = models.Member.objects.get(virtualid=virtualid)
            models.Request.objects.create(
                group=group_obj, sender=q_header, receiver=q_receiver, action=0)
        return JsonResponse({'msg': f'create group {group_obj.group_name} success waiting for accept from another member'})


class AllGroup(APIView):
    def get(self, request):
        try:
            query = models.Group.objects.filter(
                is_active=True)
            d = dict()
            l = []
            for value in query:
                q_group_member = models.GroupMember.objects.filter(
                    group=value.id).filter(role='m')
                q_header = models.GroupMember.objects.filter(
                    group=value.id).filter(role='h')[0]

                member_list = []
                for innner_value in q_group_member:
                    member_list.append({'id': innner_value.member.virtualid,
                                        'firstname': innner_value.member.first_name
                                        })
                detail_dict = dict({'announce': value.announce,
                                    'member': member_list
                                    })

                l.append({'group_name': value.group_name,
                          'header': q_header.member.first_name,
                          'public': value.is_public,
                          'detail': detail_dict if value.is_public is True else {}
                          })

            d['data'] = l
            return JsonResponse(d)
        except Exception as e:
            print(f'Error {e}')
            return JsonResponse({'message': 'Error(GET)'}, safe=False)


class MyGroup(APIView):
    def get(self, request, groupname):
        try:
            groupname = urllib.parse.unquote_plus(groupname)
            mygroup = models.Group.objects.get(group_name=groupname)
            groupid = mygroup.id
            is_member = group.group_mem_per(
                groupid=groupid, memberid=request.user.id)
            is_header = group.group_head_per(
                groupid=groupid, memberid=request.user.id)
            if is_member:
                if is_header:
                    role = 'header'
                else:
                    role = 'member'
            else:
                if request.user.id is not None:
                    if models.GroupMember.objects.filter(role='j').filter(member_id=request.user.id).filter(
                            group_id=groupid).exists():
                        role = 'waiting'
                    else:
                        role = 'free'
                else:
                    role = 'guest'

            q_group_member = models.GroupMember.objects.filter(
                group_id=groupid).filter(role='m')
            q_group_header = models.GroupMember.objects.filter(
                group_id=groupid).filter(role='h')[0]

            member_list = []

            if role == 'header':
                for innner_value in q_group_member:
                    member_list.append({'id': innner_value.member.virtualid,
                                        'firstname': innner_value.member.first_name,
                                        'delete': False
                                        })
            else:
                for innner_value in q_group_member:
                    member_list.append({'id': innner_value.member.virtualid,
                                        'firstname': innner_value.member.first_name
                                        })

            d = dict()
            d = {'group_name': mygroup.group_name,
                 'header': q_group_header.member.first_name,
                 'public': mygroup.is_public,
                 'role': role,
                 'detail': {}
                 }

            if mygroup.is_public is True or is_header or is_member:
                d['detail']['announce'] = mygroup.announce
                d['detail']['member'] = member_list

            return JsonResponse(d)
        except Exception as e:
            print(f'Error {e}')
            return JsonResponse({'message': 'Error(GET)'}, safe=False)

    def post(self, request, groupname):
        try:
            groupname = urllib.parse.unquote_plus(groupname)
            if request.user.id is not None:
                mygroup = models.Group.objects.get(group_name=groupname)
                groupid = mygroup.id
                mem = models.Member.objects.get(pk=request.user.id)
                header = models.GroupMember.objects.filter(
                    group=mygroup).filter(role='h')[0].member
                is_member = group.group_mem_per(
                    groupid=groupid, memberid=request.user.id)
                is_header = group.group_head_per(
                    groupid=groupid, memberid=request.user.id)
                if is_header or is_member:
                    return JsonResponse({'msg': "You're already in this group"})

                obj, created = models.GroupMember.objects.get_or_create(
                    group=mygroup, member=mem, role='j')
                if created:
                    models.Request.objects.create(
                        sender=mem, receiver=header, action=1, group_id=obj.group_id)
                    return JsonResponse({'msg': 'join success waiting for accept from header this group'})
                else:
                    q_request = models.Request.objects.filter(
                        sender=mem, receiver=header, action=1, group_id=obj.group_id, read=0)
                    q_request.delete()
                    obj.delete()
                    return JsonResponse({'msg': 'cancel joining this group success'})
            else:
                return JsonResponse({'msg': 'pls login first'})
        except Exception as e:
            print(e)
            return JsonResponse({'msg': 'Error'})

    def put(self, request, groupname):
        groupname = urllib.parse.unquote_plus(groupname)
        mygroup = models.Group.objects.get(group_name=groupname)
        groupid = mygroup.id
        is_header = group.group_head_per(
            groupid=groupid, memberid=request.user.id)
        if is_header:
            data = request.data
            public = data['public']
            if public is True or public is False:
                print('pass')
                print(public)
                print(mygroup.is_public)
                mygroup.is_public = public
                print(mygroup.is_public)
                mygroup.save()
                return JsonResponse({'msg': 'ok'}, status=200)
            else:
                return JsonResponse({'msg': 'true or false value only'})
        else:
            return JsonResponse({'msg': 'permission denied'}, status=400)

    def delete(self, request, groupname):
        try:
            groupname = urllib.parse.unquote_plus(groupname)
            if request.user.id is not None:
                mygroup = models.Group.objects.get(group_name=groupname)
                groupid = mygroup.id

                is_member = group.group_mem_per(
                    groupid=groupid, memberid=request.user.id)
                is_header = group.group_head_per(
                    groupid=groupid, memberid=request.user.id)

                if is_member or is_header:
                    if is_header:
                        virtualid = request.data['id']
                        member = models.Member.objects.get(virtualid=virtualid)
                        msg = 'delete member'
                    else:
                        member = models.Member.objects.get(id=request.user.id)
                        msg = 'leave group'
                    q_gm = models.GroupMember.objects.get(
                        group=mygroup, role='m', member=member)
                    q_gm.delete()
                    return JsonResponse({'msg': f'{msg} successful'})
                else:
                    return JsonResponse({'msg': 'You dont have permission !!!'})

        except Exception as e:
            print(e)
            return JsonResponse({'msg': 'Error'})


class Request(APIView):

    def get(self, request):
        try:
            if request.user.id is not None:
                query = models.Request.objects.filter(
                    receiver=request.user).filter(read=False)
                mydict = dict()
                l = list()
                for i in query:
                    if i.action == 0:
                        msg = 'accept create group'
                    elif i.action == 1:
                        msg = 'join group'
                    else:
                        msg = ''
                    l.append(
                        {'id': i.id, 'sender': i.sender.first_name, 'msg': msg, 'group': i.group.group_name})
                mydict['data'] = l
                return JsonResponse(mydict)
            return HttpResponse('Pls login (GET)')
        except Exception as e:
            print('error = ', e)
            return HttpResponse('Error (GET)')

    def post(self, request):
        try:
            if request.user.id is not None:
                myid = request.data['id']
                accept = request.data['accept']
                query = models.Request.objects.get(pk=myid)
                q_group = models.Group.objects.get(pk=query.group_id)
                if query.read == True:
                    return JsonResponse({'msg': 'try again'}, status=400)
                if query.action == 0:  # accept create group
                    if accept is True:
                        if request.user.id == query.receiver.id:
                            pass
                        else:
                            return JsonResponse({'msg': 'you not have permission'}, status=400)
                        q_allcourt = booking_models.AllCourtInfo.objects.all()[
                            0]
                        number_creategroup = q_allcourt.num_of_creategroup
                        mem = models.Member.objects.get(pk=query.receiver)

                        obj, created = models.GroupMember.objects.get_or_create(
                            group=q_group, member=mem, role='m')
                        if created:
                            query.read = 1
                            query.save()
                        if len(models.GroupMember.objects.filter(role='m').filter(group=q_group)) == number_creategroup:
                            q_group.is_active = True
                            q_group.save()
                    else:
                        q_group.delete()

                elif query.action == 1:  # accept join group
                    if group.group_head_per(memberid=request.user.id, groupid=q_group.id):
                        q_gm = models.GroupMember.objects.get(
                            member_id=query.sender, group_id=q_group.id, role='j')

                        if accept is True:
                            q_gm.role = 'm'
                            q_gm.save()
                            query.read = 1
                            query.save()
                        else:
                            q_gm.delete()
                            query.read = 1
                            query.save()
                    else:
                        return JsonResponse({'msg': 'you not have permission (header only)'}, status=400)

                return JsonResponse({'msg': 'ok'})
            return JsonResponse({'msg': 'pls login'})

        except Exception as e:
            print('error = ', e)
            return HttpResponse('Error (POST)')
