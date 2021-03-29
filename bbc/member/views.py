from . import models
from booking import models as booking_models
from . import serializers as s
from .form import LoginForm
from . import token
from . import group

from datetime import date
import json

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

        # my_data = JSONParser().parse(request)

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
            return JsonResponse({'username': username})
            # return JsonResponse({'login successfully': f'HI {auth}'}, status=200)
        else:
            return JsonResponse({'message': 'try again'}, status=404)


# @login_required(login_url='/login/')
def Logout(request):
    try:
        print('going to logout')
        logout(request)
        print('logouted')
        return JsonResponse({'message': 'logout successfully'}, status=200)
        # return HttpResponse('ok logouted')
    except Exception as e:
        print(e)
        return JsonResponse({'message': 'error'}, status=404)


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
            mem_q = models.Member.objects.filter(is_active=True)
            mem_s = s.CreateGroupMemberSerializer(mem_q, many=True)
            return JsonResponse(mem_s.data, safe=False)
        except Exception as e:
            print(f'Error = {e}')
            return JsonResponse({'message': 'Error (GET)'})

    def post(self, request):
        q_other = booking_models.OtherDetail.objects.get(pk=1)
        number_creategroup = q_other.n_member_creategroup
        if request.user.id is None:
            return JsonResponse({'message': 'Login before create group'})
        else:
            pass

        header = models.Member.objects.get(username=request.user)

        member = request.data['member']
        group_name = request.data['group_name']

        print(len(member))
        print(number_creategroup)
        if len(member) != number_creategroup:
            return JsonResponse({'message': f'Error create group with {number_creategroup} member!!!'})

        for value in member:
            if models.Member.objects.filter(username=value).exists():
                pass
            else:
                return JsonResponse({'message': f'Error this user {value} not found'}, status=404)

        obj, create = models.Group.objects.get_or_create(
            group_name=group_name, header=header, is_active=True)

        if not create:
            return JsonResponse({'message': f'Error this group name {obj.group_name} exists '}, status=400)

        for value in member:
            username = value
            receiver = models.Member.objects.get(username=username)
            models.Request.objects.create(
                sender=header, receiver=receiver, action=0, group_id=obj.id)
        return JsonResponse({'message': f'create group {obj.group_name} success waiting for accept from another member'})


class AllGroup(APIView):
    def get(self, request):
        try:
            query = models.Group.objects.filter(is_active=True)
            d = dict()
            l = []
            for value in query:
                q_group_member = models.GroupMember.objects.filter(
                    group=value.id)
                inner_list = []
                for innner_value in q_group_member:
                    inner_list.append(innner_value.member.first_name)

                l.append({'group_name': value.group_name,
                          'header': value.header.first_name,
                          'detail': value.outside_detail,
                          'member': inner_list
                          })
            d['data'] = l
            return JsonResponse(d)
        except Exception as e:
            print(f'Error {e}')
            return JsonResponse({'message': 'Error(GET)'}, safe=False)


class MyGroup(APIView):
    def get(self, request, groupname):
        try:
            mygroup = models.Group.objects.get(group_name=groupname)
            groupid = mygroup.id
            if group.group_mem_per(groupid=groupid, memberid=request.user.id):
                detail = mygroup.inside_detail
                if group.group_head_per(groupid=groupid, memberid=request.user.id):
                    role = 'header'
                else:
                    role = 'member'
            else:
                detail = mygroup.outside_detail
                if request.user.id is not None:
                    if models.GroupMember.objects.filter(role='j').filter(member_id=request.user.id).filter(
                            group_id=groupid).exists():
                        role = 'join'
                    else:
                        role = 'not member in this group'
                else:
                    role = 'guest'

            q_group_member = models.GroupMember.objects.filter(
                group_id=groupid)
            inner_list = []
            for innner_value in q_group_member:
                inner_list.append(innner_value.member.first_name)

            d = dict()
            d = {'group_name': mygroup.group_name,
                 'header': mygroup.header.first_name,
                 'detail': detail,
                 'member': inner_list,
                 'role': role
                 }

            return JsonResponse(d)
        except Exception as e:
            print(f'Error {e}')
            return JsonResponse({'message': 'Error(GET)'}, safe=False)

    def post(self, request, groupname):
        try:
            if request.user.id is not None:
                mygroup = models.Group.objects.get(group_name=groupname)
                groupid = mygroup.id
                mem = models.Member.objects.get(pk=request.user.id)

                obj, created = models.GroupMember.objects.get_or_create(
                    group=mygroup, member=mem, role='j')
                if created:
                    models.Request.objects.create(
                        sender=mem, receiver=mygroup.header, action=0, group_id=obj.group_id)
                    return JsonResponse({'msg': 'join success waiting for accept from header this group'})
                else:
                    return JsonResponse({'msg': 'try again'})
            else:
                return JsonResponse({'msg': 'pls login first'})
        except Exception as e:
            print(e)
            return JsonResponse({'msg': 'Error'})

    def delete(self, request, groupname):
        try:
            if request.user.id is not None:
                mygroup = models.Group.objects.get(group_name=groupname)
                groupid = mygroup.id
                q = models.GroupMember.objects.filter(
                    group=groupid).filter(role='m').exists()
        except Exception as e:
            pass


class Request(APIView):

    def get(self, request):
        try:
            if request.user.id is not None:
                query = models.Request.objects.filter(
                    receiver=request.user).filter(state=False)
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
                        {'id': i.id, 'sender': i.sender.first_name, 'msg': msg})
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
                query = models.Request.objects.get(pk=myid)
                q_group = models.Group.objects.get(pk=query.group_id)

                if query.action == 0:  # accept create group
                    q_other = booking_models.OtherDetail.objects.get(pk=1)
                    number_creategroup = q_other.n_member_creategroup
                    mem = models.Member.objects.get(pk=request.user.id)

                    obj, created = models.GroupMember.objects.get_or_create(
                        group=q_group, member=mem, role='m')
                    if created:
                        q_group.count += 1
                        q_group.save()
                        query.state = 1
                        query.save()

                    if q_group.count == number_creategroup:
                        q_group.is_active = True
                        q_group.save()

                elif query.action == 1:  # accept join group

                    if group_head_per(member=request.user.id, groupid=q_group.id):
                        q_gm = models.GroupMember.objects.get(
                            member_id=query.sender, group_id=q_group.id)

                        if q_gm.role == 'j':
                            q_gm.ipdate(role='m')
                            query.state = 1
                            query.save()
                    else:
                        return JsonResponse({'msg': 'you not have permission (header only)'})

                return JsonResponse({'msg': 'ok'})
            return JsonResponse({'msg': 'pls login'})

        except Exception as e:
            print('error = ', e)
            return HttpResponse('Error (POST)')


# class Mygroup(APIView):
#     def get(self, request, groupid):
#         try:
#             id_ = groupid
#             # mem = models.Member.objects.get(pk=request.user.id)
#             # print(f'query member success = {mem.mygroup.group_name}')
#             # query = models.GroupMember.objects.filter(
#             #     group_name=mem.mygroup.group_name).filter(member=request.user.id)  # .exists()
#             # print('check groupmember success')
#             # group = models.Group.objects.get(pk=mem.mygroup.id)
#             # print('check group success')
#             # print(f'query = {group}')
#             # query = models.Group.objects.filter(is_active=True)
#             # s_query = s.MygroupSerializer(group)
#             # print(f's_query.data ={s_query.data}')
#             # # return JsonResponse(s_query.data, safe=False)
#             # t = models.GroupMember.objects.filter(
#             #     group_name=mem.mygroup.group_name)
#             # ts = s.GroupmemberSerializer(t, many=True)
#             # print(f't = {t}')
#             # print(f'ts = {ts.data}')
#             # return JsonResponse(ts.data, safe=False)
#             return JsonResponse({'message': f'ok get {id_}'})
#         except Exception as e:
#             print(f'Error {e}')
#             return JsonResponse({'message': 'Error(GET)'}, safe=False)

#     def post(self, request):
#         try:

#             return JsonResponse({'message': 'OK (POST)'}, safe=False)
#         except Exception as e:
#             print(f'Error {e}')
#             return JsonResponse({'message': 'Error(POST)'}, safe=False)


# class Mygroup(APIView):
#     def get(self, request):
#         try:
#             mem = models.Member.objects.get(pk=request.user.id)
#             print(f'query member success = {mem.mygroup.group_name}')
#             query = models.GroupMember.objects.filter(
#                 group_name=mem.mygroup.group_name).filter(member=request.user.id)  # .exists()
#             print('check groupmember success')
#             group = models.Group.objects.get(pk=mem.mygroup.id)
#             print('check group success')
#             print(f'query = {group}')
#             query = models.Group.objects.filter(is_active=True)
#             s_query = s.MygroupSerializer(group)
#             print(f's_query.data ={s_query.data}')
#             # return JsonResponse(s_query.data, safe=False)
#             t = models.GroupMember.objects.filter(
#                 group_name=mem.mygroup.group_name)
#             ts = s.GroupmemberSerializer(t, many=True)
#             print(f't = {t}')
#             print(f'ts = {ts.data}')
#             return JsonResponse(ts.data, safe=False)
#         except Exception as e:
#             print(f'Error {e}')
#             return JsonResponse({'message': 'Error(GET)'}, safe=False)

#     def post(self, request):
#         try:

#             return JsonResponse({'message': 'OK (POST)'}, safe=False)
#         except Exception as e:
#             print(f'Error {e}')
#             return JsonResponse({'message': 'Error(POST)'}, safe=False)


# @login_required(login_url='/login/')
# def Mygroup(request):
#     try:
#         print(request.user.id)
#         mem = models.Member.objects.get(pk=request.user.id)
#         print(f'query member success {mem.mygroup.group_name}')
#         models.GroupMember.objects.filter(
#             group_name=mem.mygroup.group_name).filter(member=request.user.id)  # .exists()
#         print('check groupmember success')
#         group = models.Group.objects.get(pk=mem.mygroup.id)
#         print('check group success')
#         mydict = list()
#         mydict.append({
#             'group_name': group.group_name,
#             'header': group.header.first_name,
#             'inside_detail': group.inside_detail,
#             'payed': group.is_continue
#         })
#         print(mydict)
#         print('before return')
#         return HttpResponse(json.dumps(mydict), content_type='application/json')
#         # return JsonResponse(json.dumps(mydict), safe=False)
#     except Exception as e:
#         print(e)
#         return JsonResponse({'message': 'error'})


# @ api_view(['GET', 'POST'])
# def testget(request):
#     try:
#         print(request.user)
#         if request.method == 'GET':
#             return HttpResponse('OK (GET)')
#         if request.method == 'POST':
#             return HttpResponse('OK (POST)')
#     except Exception as e:
#         print(e)
#         return HttpResponse('Error')


# @login_required(login_url='/login/')
# def Profile(request):
#     try:
#         print(request.user)
#         user_id = request.user.id
#         print(type(user_id))
#         user_id = str(user_id)
#         print(user_id)
#         print(models.Member.objects.get(username=request.user))

#         member = models.Member.objects.get(pk=request.user.id)
#         mem_serializer = s.MemberSerializer(member)
#         print(mem_serializer)
#         return JsonResponse(mem_serializer.data, safe=False)
#     except:
#         return HttpResponse('error')
    # return HttpResponse('you are user_id =  {}'.format(user_id))

# @login_required(login_url='/login/')
# def Listgroup(request):
#     try:
#         query = models.Group.objects.filter(is_active=True)
#         test = s.ListgroupSerializer(query, many=True)
#         return JsonResponse(test.data, safe=False)
#         # return HttpResponse(test.data, content_type='application/json')
#     except Exception as e:
#         print(e)
#         return HttpResponse('error')


# @api_view(['GET', 'POST'])
# def Login(request):
#     try:
#         if request.method == 'POST':
#             user_login = authenticate(
#                 request, username=request.data['username'], password=request.data['password'])
#             print('my test = ', user_login)
#             print('test = ', user_login.pk)
#             if user_login is not None:
#                 login(request, user_login)
#                 session = request.session._session_key
#                 member = models.Member.objects.get(pk=request.user.id)
#                 mem_serializer = s.MemberSerializer(member)
#                 # return JsonResponse(mem_serializer, safe=False)
#                 return JsonResponse({'accessToken': session, 'username': member.username}, safe=False)
#                 # return HttpResponse('ok!!!')
#             else:
#                 # member = models.Member.objects.get(pk=request.user.id)
#                 # mem_serializer = s.MemberSerializer(member)
#                 # return JsonResponse(mem_serializer.data, safe=False)
#                 return JsonResponse({'message': 'username or password not correct!!!'})
#                 # return HttpResponse('try again!!!')
#         else:
#             return render(request, 'login.html', {'form': LoginForm})
#             # return HttpResponse('POST method only !!!')
#     except Exception as e:
#         print(e)
#         return HttpResponse('try again2!!!')


# creategroup
    # def post(self, request):
    #     try:
    #         r = request.user.id
    #         # r = 10
    #         member1 = request.data['member1']
    #         member2 = request.data['member2']
    #         member3 = request.data['member3']
    #         group_name = request.data['group_name']
    #         models.Member.objects.get(username=member1)
    #         models.Member.objects.get(username=member2)
    #         models.Member.objects.get(username=member3)
    #         print(models.Member.objects.get(pk=r).id)
    #         print(type(request.user.id))
    #         print(type(member1))
    #         print('ok check member in db success')
    #         if not models.Group.objects.filter(group_name=group_name).exists() and not models.Group.objects.filter(header=r).exists():
    #             print('1')
    #             print("let's create group")
    #             print(models.Member.objects.get(pk=r))
    #             print(type(models.Member.objects.get(pk=r)))
    #             # models.Group(group_name=group_name,
    #             #              header=models.Member.objects.get(pk=r), outside_detail='out', inside_detail='in').save()
    #             mygroup = models.Group(group_name=group_name,
    #                                    header=models.Member.objects.get(pk=r), outside_detail='out', inside_detail='in')
    #             mygroup.is_active = True
    #             mygroup.save()
    #             print('create pass')
    #             # models.RequestMember(sender=models.Group.objects.get(header=r),
    #             #                      reveiver=models.Member.objects.get(username=member1), action=0).save()
    #             # models.RequestMember(sender=models.Group.objects.get(header=r),
    #             #                      reveiver=models.Member.objects.get(username=member2), action=0).save()
    #             # models.RequestMember(sender=models.Group.objects.get(header=r),
    #             #                      reveiver=models.Member.objects.get(username=member3), action=0).save()
    #             return JsonResponse({'message': 'ok Create group success'})
    #         return JsonResponse({'message': 'Error >>> Group name is already use or You have already created a group.'})
    #     except Exception as e:
    #         print(f'Error = {e}')
    #         return JsonResponse({'message': 'Error (GET)'})

    # @csrf_exempt
# @api_view(['GET', 'POST'])
# def Creategroup(request):
#     try:
#         r = request.user.id
#         #r = 10
#         member1 = request.data['member1']
#         member2 = request.data['member2']
#         member3 = request.data['member3']
#         group_name = request.data['group_name']
#         models.Member.objects.get(pk=member1)
#         models.Member.objects.get(pk=member2)
#         models.Member.objects.get(pk=member3)
#         print(models.Member.objects.get(pk=r).id)
#         print(type(request.user.id))
#         print(type(member1))
#         print('ok check member in db success')
#         if not models.Group.objects.filter(group_name=group_name).exists():
#             print('1')
#             print("let's create group")
#             # print(models.Member.objects.get(pk=r))
#             # print(type(models.Member.objects.get(pk=r)))
#             # models.Group(group=group_name,
#             #              header=models.Member.objects.get(pk=r), outside_detail='out', inside_detail='in').save()
#             # models.Group(group=group_name,
#             #              header=models.Member.objects.get(pk=r), outside_detail='out', inside_detail='in', is_active=True).save()
#             # models.RequestMember(header=models.Group.objects.get(header=r),
#             #                      member=models.Member.objects.get(pk=member1), action=0).save()
#             # models.RequestMember(header=models.Group.objects.get(header=r),
#             #                      member=models.Member.objects.get(pk=member2), action=0).save()
#             # models.RequestMember(header=models.Group.objects.get(header=r),
#             #                      member=models.Member.objects.get(pk=member3), action=0).save()
#             mem_q = models.Member.objects.filter(is_active=True)
#             print('q success')
#             mem_s = s.CreateGroupMemberSerializer(mem_q, many=True)
#             print('s success')
#             print(mem_s.data)
#             return JsonResponse(mem_s.data, safe=False)
#             # return JsonResponse({'message': 'ok'})
#         return JsonResponse({'message': 'group name is exists'})
#     except Exception as e:
#         print(e)
#         return JsonResponse({'message': 'error'})
