from django.shortcuts import render
from .models import *
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.hashers import make_password
import random
import smtplib
from email.mime.text import MIMEText
from django.http import HttpResponse
# Create your views here.
@csrf_exempt
def register_views(request):
    return render(request, 'register_00.html')

@csrf_exempt
def register_db_views(request):
    global nickname, uname, upwd
    user = User.objects.filter(name=uname)
    if user:
        pass
    else:
        upwd = make_password(upwd, None,'pbkdf2_sha256')
        email_accept = request.POST['choose']
        User.objects.create(name=uname, nickname=nickname, pwd=upwd, accept=email_accept)
    return render(request, 'register_05.html', locals())

@csrf_exempt
def register_01_views(request):
    global ver, nickname, uname, upwd
    ver = ''
    while True:
        ver += str(random.randint(0, 9))
        if len(ver) == 6:
            break
    mailto = uname
    mail_host = "smtp.qq.com"  # 使用的邮箱的smtp服务器地址，这里是163的smtp地址
    mail_user = "pandaweather"  # 用户名
    mail_pass = "lalfajxlfidzbhii"  # 密码
    mail_postfix = "qq.com"
    ver_msg = '欢迎使用Panda Weather!您的注册验证码为' + ver
    def send_mail(to_list,sub,content):
        me="Panda Weather" + "<" + mail_user + "@" + mail_postfix + ">" # me=pandaweather@163.com
        msg = MIMEText(content,_subtype='plain')
        msg['Subject'] = sub
        msg['From'] = me
        msg['To'] = mailto
        server = smtplib.SMTP()
        server.connect(mail_host)                       #连接服务器
        server.login(mail_user,mail_pass)               #登录操作
        server.sendmail(me, to_list, msg.as_string())
        server.close()
    send_mail(mailto, "Panda Weather用户注册", ver_msg)
    return render(request, 'register_01.html', locals())

@csrf_exempt
def register_02_views(request):
    global ver
    if ver == request.POST['verification']:
        return render(request, 'register_02.html', locals())
    else:
        return render(request, 'register_03.html', locals())

@csrf_exempt
def register_03_views(request):
    global nickname, uname, upwd
    nickname = request.POST['nickname']
    uname = request.POST['uname']
    upwd = request.POST['upwd']
    is_exist = User.objects.filter(name__exact=uname)
    if is_exist:
        return render(request, "register_04.html") # 如果改邮箱注册过
    else:
        return register_01_views(request) # 没注册过