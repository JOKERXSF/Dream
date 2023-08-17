import random

from django.http import JsonResponse
from django.template import loader, Context
from django.core.mail import EmailMessage
from 梦想通招聘分析.settings import EMAIL_HOST_USER
from Dreamapp.models import User


def checkuname(request):
    res = {'user': None, 'msg': None}
    username = request.GET.get('username')
    user_obj = User.objects.filter(username=username).first()
    if user_obj:
        res['msg'] = '该用户已注册'
        return JsonResponse(res)
    else:
        res['user'] = username
        return JsonResponse(res)


def send_email(subject,html_content, recipient_list):
    msg = EmailMessage(subject, html_content, EMAIL_HOST_USER, recipient_list)
    msg.content_subtype = "html"
    msg.send()


def ValueCode():
    randomstr = ''
    for i in range(4):
        dig = str(random.randint(0, 9))
        low = chr(random.randint(97, 122))
        up = chr(random.randint(65, 90))
        code = random.choice([dig, low, up])
        randomstr += code

    return randomstr

# if __name__ == '__name__':
#     template_path = 'login.html'
#     html_content = loader.render_to_string(
#
#         # template_path,
#
#         {'paramters':'123456'}
#     )
#     send_email(u'梦想通激活邮件', html_content, ['1426438143@qq.com',])
