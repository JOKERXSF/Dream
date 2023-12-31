from itsdangerous import TimedJSONWebSignatureSerializer as Serializer, BadData
from django.conf import settings
from django.contrib.auth.tokens import default_token_generator
from django.shortcuts import render, redirect
from Dreamapp.models import User
from .utils.error import *
from django.views import View
from django.http import JsonResponse
from .models import *
from django.contrib import auth
from django.template import loader, Context
from . import ut
from django.core.mail import send_mail, send_mass_mail
import hashlib
from .utils import getHomeData
from .utils import getSelfInfo
from .utils import getcompanyCharData
from .utils import getChangePasswordData


# Create your views here.
# 主界面跳转
# def home(request):
#     uname = request.session.get('username')
#     userInfo = User.objects.get(username=uname)
#     year, month, day = getHomeData.getNowTime()
#     userCreateData = getHomeData.getUserCreateTime()
#     top6Users = getHomeData.getUserTop6()
#     jobsLen,usersLen,educationsTop,salaryTop,salaryMonthTop,addressTop,praticeMax = getHomeData.getAllTags()
#     jobsPBarData = getHomeData.getAllJobsPBar()
#     tablaData = getHomeData.getTablaData()
#
#     print(year, month, day)
#     return render(request, 'index.html', {
#         'userInfo': userInfo,
#         'dateInfo': {
#             'year': year,
#             'month': month,
#             'day': day
#         },
#         'userCreateData':userCreateData,
#         'top6Users':top6Users,
#         'tagDic':{
#             'jobsLen':jobsLen,
#             'usersLen':usersLen,
#             'educationsTop':educationsTop,
#             'salaryTop':salaryTop,
#             'addressTop':addressTop,
#             'salaryMonthTop':salaryMonthTop,
#             'praticeMax':praticeMax
#         },
#         'jobsPBarData':jobsPBarData,
#         'tableData':tablaData
#     })


# 登录界面

def home(request):
    uname = request.session.get('username')
    userInfo = User.objects.get(username=uname)
    year, month, day = getHomeData.getNowTime()
    print(year, month, day)
    return render(request, 'index.html', {
        'userInfo': userInfo,
        'dateInfo': {
            'year': year,
            'month': month,
            'day': day
        }
    })


def login(request):
    if request.method == 'POST':
        uname = request.POST.get('username')
        pwd = request.POST.get('password')
        print(uname, pwd)
        # md5 = hashlib.md5()
        # md5.update(pwd.encode())
        # pwd = md5.hexdigest()
        user = User.objects.get(username=uname, password=pwd)
        print(user)

        if user is not None:
            request.session['username'] = user.username
            return redirect('/Dreamapp/home/')
        else:
            return redirect('/Dreamapp/login/')

    else:
        return render(request, 'login.html')


# def registry(request):
#     if request.method == "GET":
#         return render(request,'registry.html')
#     else:
#         uname = request.POST.get('username')
#         passw = request.POST.get('password')
#         ema = request.POST.get('email')
#         try:
#             User.objects.get(username=uname)
#         except:
#             if not uname or not passw or not ema:return errorResponse(request,'不允许为空！')

# class loginView(View):
#
#     def get(self, request):
#         return render(request, 'login.html')
#
#     def post(self, request):
#         res = {'user': None, 'msg': None}
#         username = request.POST.get('username')
#         pwd = request.POST.get('pwd')
#
#         user = auth.authenticate(username=username, password=pwd)
#
#         if user:
#             if user.is_active == 1:
#                 res['user'] = "1"
#                 res['msg'] = '登录成功'
#                 request.session['username'] = username
#                 return JsonResponse(res)
#             else:
#                 res['user'] = "0"
#                 res["msk"] = '该账户还未激活请前往邮箱激活'
#                 request.session['username'] = username
#                 return JsonResponse(res)
#         else:
#             res['msg'] = '用户名或密码错误'
#             return JsonResponse(res)


# 注册界面
class registryView(View):

    def get(self, request):
        return render(request, 'registry.html')

    def post(self, request):
        res = {'user': None, 'msg': None}
        username = request.POST.get('username')
        pwd = request.POST.get('pwd')
        email = request.POST.get('email')

        print(username, pwd, email)

        m = User.objects.create(username=username, password=pwd, email=email, is_active=0)

        res['user'] = username
        return JsonResponse(res)


# class ActiveAccount(View):
#
#     def get(self,request):
#         code = ut.ValueCode()
#
#         request.session['code'] = code
#         username = request.session.get('username')
#         user_obj = User.objects.filter(username=username).first()
#         email = user_obj.email
#
#
#         template_path = '../templates/code.html'
#         html_content = loader.render_to_string(
#
#             template_path,
#
#             {'code',code}
#         )
#
#         ut.send_email(u'梦想通激活邮件',html_content,[email])
#         return render(request,'active.html',{'code':code})
#
#     def post(self,request):
#         res = {'status':None,'msg':None}
#         code = request.POST.get('code')
#         if code == request.session.get('code'):
#             res['msg'] = '激活成功'
#             res['status'] = '0'
#             username = request.session.get('username')
#             user = User.objects.filter(username=username).first()
#             user.is_active = True
#             user.save()
#         else:
#             res['msg'] = '激活失败'
#             res['status'] = '1'
#
#         return JsonResponse(res)
# 发送邮箱
def reset_password(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            # 用户不存在的处理逻辑
            return redirect('/Dreamapp/reset_password')

        serializer = Serializer(settings.SECRET_KEY, expires_in=3600)
        data = {'username': user.username, 'email': user.email}
        token = serializer.dumps(data).decode()

        reset_link = request.build_absolute_uri(
            f'/Dreamapp/password_reset/{user.pk}/{token}/'
        )
        context = {
            'user_pk': user.pk,
            'token': token,
        }
        send_mail(
            '重置密码',
            f'请点击以下链接重置密码：{reset_link}',
            '1203200361@qq.com',
            [email],
            fail_silently=False,
        )

        # 发送邮件成功的处理逻辑
        return redirect('/Dreamapp/reset_password')

    return render(request, 'reset_password.html')


# 邮箱验证界面
def reset_password_confirm(request, user_pk, token):
    serializer = Serializer(settings.SECRET_KEY, expires_in=3600)
    try:
        data = serializer.loads(token)
    except BadData:
        # 用户不存在的处理逻辑
        return redirect('/Dreamapp/reset_password')
    else:
        username = data.get('username')
        email = data.get('email')
        user = User.objects.get(email=email)

    if request.method == 'POST':
        password = request.POST.get('password')
        password_confirm = request.POST.get('password_confirm')

        if password != password_confirm:
            # 两次输入的密码不一致地处理逻辑
            return redirect('reset_password_confirm', user_pk=user_pk, token=token)

        user.password = password
        user.save()

        # 密码重置成功的处理逻辑
        return redirect('/Dreamapp/login')

    return render(request, 'reset_password_confirm.html', {'user_pk': user_pk, 'token': token})


# 登出
def logOut(request):
    request.session.clear()
    return redirect('login')


# 个人信息
def selfInfo(request):
    uname = request.session.get('username')
    userInfo = User.objects.get(username=uname)
    educational, workExperience, jobsTypes = getSelfInfo.getPageData()
    if request.method == 'POST':
        getSelfInfo.changeSelfInfo(request.POST, request.FILES)
        userInfo = User.objects.get(username=uname)
    return render(request, 'selfInfo.html', {
        'userInfo': userInfo,
        'pageData': {
            'educational': educational,
            'workExperience': workExperience,
            'jobsTypes': jobsTypes
        }
    })


# 修改密码功能
def changePassword(request):
    uname = request.session.get('username')
    userInfo = User.objects.get(username=uname)
    if request.method == 'GET':
        return render(request,'changePassword.html',{
            'username': uname,
            'userInfo': userInfo,
        })
    else:
        res = getChangePasswordData.changePassword(request.POST,userInfo)
        if res != None:
            return redirect('changePassword')
        userInfo = User.objects.get(username=uname)
        return render(request, 'changePassword.html', {
            'username': uname,
            'userInfo': userInfo,
        })


# 公司情况
def company(request):
    uname = request.session.get('username')
    userInfo = User.objects.get(username=uname)
    typeList = getcompanyCharData.getPageData()
    type = 'all'
    if request.GET.get('type'): type = request.GET.get('type')

    return render(request, 'companyChar.html', {
        'userInfo': userInfo,
        'typeList': typeList
    })

#公司福利
def companyTags(request):
    uname = request.session.get('username')
    userInfo = User.objects.get(username=uname)
    return render(request, 'companyTags.html', {
        'userInfo': userInfo
    })