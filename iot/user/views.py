import hashlib
import json
from codecs import encode

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.shortcuts import render
userLogin = login
userLogout = logout

# Create your views here.

def add(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        email = request.POST['email']

        try:
            User.objects.get(username=username)
            response = {
                'error': -1,
                'error': '用户名已存在',
            }
            return JsonResponse(response)
        except User.DoesNotExist:
            # code = hashlib.pbkdf2_hmac('sha256', bytes(password,'UTF-8'), b'123456723456', 500)
            user = User.objects.create(username=username)
            user.set_password(password)
            user.save()
            response = {
                'error': 0,
                'msg': '添加成功'
            }
            return JsonResponse(response)

def login(request):
    if request.method == 'POST':
        msg = json.loads(request.body)
        print(msg)
        username = msg['username']
        password = msg['password']
        # code = hashlib.md5()
        # code.update(password.encode(encoding='utf-8'))
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                userLogin(request, user)
                response = {
                    'error': 0,
                    'msg': '已登陆',
                    'session': request.session.session_key
                }
                return JsonResponse(response)
        else:
            response = {
                'error': -1,
                'msg': '登陆失败'
            }
            JsonResponse(response).set_cookie()
            return

def logout(request):
    if request.method == 'POST':
            userLogout(request)
            response = {
                'error': 0,
                'msg': '登出成功'
            }
            return JsonResponse(response)

def requestLogin(request):
    print(request)
    response = {
        'error': -1,
        'msg': '请先登陆'
    }
    return JsonResponse(response)



