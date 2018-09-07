from datetime import datetime, timedelta

from django.contrib.auth.hashers import make_password, check_password
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

from user.models import UserModel, UserTicketModel
from utils.functions import get_ticket


def register(request):
    # 注册视图函数
    if request.method == 'GET':
        # 如果是GET请求,进入注册页面
        return render(request, 'user/user_register.html')

    if request.method == 'POST':
        # 如果是POST请求需进行注册内容进行判断, 然后进入登录页面
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        icon = request.FILES.get('icon')

        # 判断以上参数是否为空
        if not all([username, email, password, icon]):
            # 如果参数为空, 给出温馨提示
            msg = '请检查信息是否填写完整'
            return render(request, 'user/user_register.html', {'msg': msg})

        # 如果信息填写完整需要对密码进行加密
        password = make_password(password)
        # 将信息添加到数据库, 并进入登录页面
        UserModel.objects.create(username=username,
                                 email=email,
                                 password=password,
                                 icon=icon)
        return HttpResponseRedirect(reverse('user:login'))


def login(request):
    # 登录视图函数
    if request.method == 'GET':
        # 如果是GET请求,进入注册页面
        return render(request, 'user/user_login.html')

    if request.method == 'POST':
        # 如果是POST请求,需进行用户信息验证
        username = request.POST.get('username')
        password = request.POST.get('password')
        data = {}
        # 验证登陆信息是否完整
        if not all([username, password]):
            data['msg'] = '信息填写不完整'
        # 验证用户是否注册
        if UserModel.objects.filter(username=username).exists():
            # 判断密码是否正确
            user = UserModel.objects.get(username=username)
            if check_password(password, user.password):
                # 保存ticket到浏览器
                ticket = get_ticket()
                response = HttpResponseRedirect(reverse('axf:mine'))
                out_time = datetime.now() + timedelta(days=1)
                response.set_cookie('ticket', ticket, expires=out_time)
                # 保存ticket到数据库表中
                UserTicketModel.objects.create(user=user,
                                               out_time=out_time,
                                               ticket=ticket)
                return response
            else:
                data['msg'] = '密码错误'
        else:
            data['msg'] = '用户名错误'
        return render(request, 'user/user_login.html', data)


def logout(request):
    if request.method == 'GET':
        response = HttpResponseRedirect(reverse('user:login'))
        response.delete_cookie('ticket')
        return response