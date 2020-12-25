from . import models
from booking import models as booking_models
from .serializers import MemberSerializer
from .form import LoginForm

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

# Create your views here.


@api_view(['GET', 'POST'])
def Index(request):
    print('hi')
    user = get_user(request)
    print(user)
    try:
        models.Member.objects.get(username=user)
        # in real use run user page template
        return HttpResponse('hi user!!! {}'.format(user))
    except:
        # in real use run normal page template
        return HttpResponse('hi guest!!!')


def Register(request):
    if request.method == 'POST':
        my_data = JSONParser().parse(request)
        print(my_data)
        username = my_data['username']
        password = my_data['password']
        firstname = my_data['firstname']
        lastname = my_data['lastname']
        email = my_data['email']
        tel = '00000221'
        birthday = '1999/03/15'
        gender = 'male'
        try:
            b = birthday.split('/')
            birth = date(int(b[0]), int(b[1]), int(b[2]))
            print(birth)
            regis = models.Member.objects.create_user(
                username=username, password=password, email=email)
            regis.first_name = firstname
            regis.last_name = lastname
            regis.tel = tel
            print('before')
            regis.birthday = birth
            print('pass')
            regis.gender = gender
            regis.save()
            print('Register Success')
            return HttpResponse("Register Success")

        except Exception as e:
            print('Error !!! >>> ', e)
            return HttpResponse('Register Error!!! ', e)

    else:
        return HttpResponse('Try Again!!!')


@api_view(['GET', 'POST'])
def Login(request):
    try:
        if request.method == 'POST':
            print('method = POST')
            username = request.data['username']
            password = request.data['password']
            print('recieved data')
            user_login = authenticate(
                request, username=username, password=password)
            if user_login is not None:
                login(request, user_login)
                print("You're login now")
                session = request.session._session_key
                print('session key : ', session)
                print('username : ', request.user)
                member = models.Member.objects.get(pk=request.user.id)
                # return JsonResponse(mem_serializer, safe=False)
                return JsonResponse({'accessToken': session, 'username': member.username}, safe=False)
                # return HttpResponse('ok!!!')
            else:
                #member = models.Member.objects.get(pk=request.user.id)
                #mem_serializer = MemberSerializer(member)
                # return JsonResponse(mem_serializer.data, safe=False)
                # return JsonResponse({'message': 'username or password not correct!!!'})
                return HttpResponse('try again!!!')
        else:
            return render(request, 'login.html', {'form': LoginForm})
            # return HttpResponse('POST method only !!!')
    except Exception as e:
        print(e)
        return HttpResponse('try again2!!!')


# @login_required(login_url='/login/')
def Profile(request):
    try:
        print(request.user)
        user_id = request.user.id
        print(type(user_id))
        user_id = str(user_id)
        print(user_id)
        print(models.Member.objects.get(username=request.user))

        member = models.Member.objects.get(pk=request.user.id)
        mem_serializer = MemberSerializer(member)
        return JsonResponse(mem_serializer.data, safe=False)
    except:
        return HttpResponse('error')
    # return HttpResponse('you are user_id =  {}'.format(user_id))


# @login_required(login_url='/login/')
def Logout(request):
    try:
        print('going to logout')
        logout(request)
        print('logouted')
        return JsonResponse({'message': 'logout successfully'}, status=status.HTTP_200_OK)
        # return HttpResponse('ok logouted')
    except Exception as e:
        print(e)


# @login_required(login_url='/login/')
def Listgroup(request):
    try:
        query = models.Group.objects.filter(is_active=True)
        mydict = list()
        for key, value in enumerate(query):
            innerquery = models.GroupMember.objects.filter(group_name=value.id)
            # print(innerquery.objects.all())
            mydict.append({'group': value.group_name,
                           'header': value.header.username,
                           'detail': value.outside_detail,
                           'allmember': [i.member.username for i in innerquery],
                           'history': 'Not yet',
                           })
        # return JsonResponse(json.dumps(mydict))
        return HttpResponse(json.dumps(mydict), content_type='application/json')
    except Exception as e:
        print(e)
        return HttpResponse('error')


@login_required(login_url='/login/')
def Mygroup(request):
    try:
        mem = models.Member.objects.get(pk=request.user.id)
        print('query member success')
        models.GroupMember.objects.filter(
            group=mem.mygroup).filter(member=mem.id)
        print('check groupmember success')
        group = models.Group.objects.get(pk=mem.mygroup.id)
        print('check group success')
        mydict = list()
        mydict.append({
            'group_name': group.group,
            'header': group.header.first_name,
            'inside_detail': group.inside_detail,
            'payed': group.is_continue
        })
        return HttpResponse(json.dumps(mydict), content_type='application/json')
        # return JsonResponse(json.dumps(mydict), safe=False)
    except Exception as e:
        print(e)
        return JsonResponse({'message': 'error'})


@csrf_exempt
@api_view(['GET', 'POST'])
def Creategroup(request):
    try:
        r = request.user.id
        #r = 10
        member1 = request.data['member1']
        member2 = request.data['member2']
        member3 = request.data['member3']
        group_name = request.data['group_name']
        models.Member.objects.get(pk=member1)
        models.Member.objects.get(pk=member2)
        models.Member.objects.get(pk=member3)
        print(models.Member.objects.get(pk=r).id)
        print(type(request.user.id))
        print(type(member1))
        print('ok check member in db success')
        if not models.Group.objects.filter(group=group_name).exists():
            print('1')
            print("let's create group")
            print(models.Member.objects.get(pk=r))
            print(type(models.Member.objects.get(pk=r)))
            models.Group(group=group_name,
                         header=models.Member.objects.get(pk=r), outside_detail='out', inside_detail='in').save()
            models.RequestMember(header=models.Group.objects.get(header=r),
                                 member=models.Member.objects.get(pk=member1), action=0).save()
            models.RequestMember(header=models.Group.objects.get(header=r),
                                 member=models.Member.objects.get(pk=member2), action=0).save()
            models.RequestMember(header=models.Group.objects.get(header=r),
                                 member=models.Member.objects.get(pk=member3), action=0).save()
            return JsonResponse({'message': 'ok'})
        return JsonResponse({'message': 'group name is exists'})
    except Exception as e:
        print(e)
        return JsonResponse({'message': 'error'})


# class Request(View):

#     @api_view(['GET', 'POST'])
#     def get(self, request):
#         # try:
#         d = request.data
#         return HttpResponse('Thsi is get method')
#         # except:
#         # return HttpResponse('Thsi is get method Error')

#     def post(self, request):
#         return HttpResponse('Thsi is post method')


class Request(APIView):

    def get(self, request):
        try:
            if request.user.id is not None:
                print(request.user)
                print(models.Request.objects.filter(receiver=request.user))
                query = models.Request.objects.filter(receiver=request.user)
                mydict = list()
                for i in query:
                    mydict.append(
                        {'sender': i.sender.username, 'action': i.action})
                print(mydict)
                # return HttpResponse(json.dumps(mydict), content_type='application/json')
                # return HttpResponse('<html> <head> </head> <body> <button type="submit" formmethod="POST"> Click Me!</button> </body> </html>')
                return HttpResponse('<html> <head> </head> <body> <form method="POST" action="/test/">{% csrf_token %}<button type="submit" >Continue</button></form> </body> </html>')
            return HttpResponse('Pls login (GET)')
        except Exception as e:
            print('error = ', e)
            return HttpResponse('Error (GET)')

    # @csrf_exempt
    def post(self, request):
        try:
            print(request.user)
            # if request.user.id is not None:
            #     myid = request.data['id']
            #     action = request.data['action']
            #     if action == 0:
            #         pass
            return HttpResponse('Ok (POST)')

        except Exception as e:
            print('error = ', e)
            return HttpResponse('Error (POST)')


@api_view(['GET', 'POST'])
def testget(request):
    try:
        print(request.user)
        if request.method == 'GET':
            return HttpResponse('OK (GET)')
        if request.method == 'POST':
            return HttpResponse('OK (POST)')
    except Exception as e:
        print(e)
        return HttpResponse('Error')
