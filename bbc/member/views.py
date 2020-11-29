from django.shortcuts import render
from .models import Member
from .serializers import MemberSerializer
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from rest_framework.decorators import api_view
from django.contrib.auth import authenticate, login, logout, get_user
from django.http.response import JsonResponse
from rest_framework.parsers import JSONParser
from datetime import date
from .form import LoginForm
# Create your views here.


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
        return HttpResponse('hi guess!!!')


def Register(request):
    if request.method == 'POST':
        my_data = JSONParser().parse(request)
        print(my_data)
        username = my_data['username']
        password = my_data['password']
        firstname = my_data['firstname']
        lastname = my_data['lastname']
        email = my_data['email']
        tel = '00000221'  # my_data['tel']
        birthday = '1999/03/15'  # my_data['birthday']
        gender = 'male'  # my_data['gender']
        # username = request.POST.get('username')
        # password = request.POST.get('password')
        # firstname = request.POST.get('first_name')
        # lastname = request.POST.get('last_name')
        # email = request.POST.get('email')
        # tel = request.POST.get('tel')
        # birthday = request.POST.get('birthday')
        # gender = request.POST.get('gender')
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
    if request.method == 'POST':
        myrequest = request
        my_data = JSONParser().parse(myrequest)
        print(type(my_data))
        print(my_data['username'])
        print('1')
        # print(request.body)
        username = my_data['username']
        password = my_data['password']
        print(username)
        print(password)
        user_login = authenticate(
            request, username=username, password=password)
        if user_login is not None:
            login(request, user_login)
            print("You're login now")
            print(request.user)
            s = request.session._session_key
            print('session key : ', s)
            print('username : ', request.user.id)
            member = Member.objects.get(pk=request.user.id)
            print(type(member))
            print(member.username)
            mem_serializer = MemberSerializer(member)

            return JsonResponse({'accessToken': s}, safe=False)
            # return HttpResponse('ok!!!')
        else:
            return JsonResponse({'message': 'username or password not correct!!!'})
            # return HttpResponse('try again!!!')
    else:
        return render(request, 'login.html', {'form': LoginForm})
        # return HttpResponse('POST method only !!!')


@ login_required(login_url='/login/')
def Profile(request):
    user_id = request.user.id
    print(type(user_id))
    user_id = str(user_id)
    print(user_id)
    print(models.Member.objects.get(username=request.user))
    return HttpResponse('you are user_id =  {}'.format(user_id))


@ login_required(login_url='/login/')
def Logout(request):
    logout(request)
    return HttpResponseRedirect('/')


@api_view(['GET', 'POST'])
def test(request):
    if request.method == 'POST':
        Member.objects.all()
