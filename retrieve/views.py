from django.shortcuts import render
import random
from django.views.decorators.csrf import csrf_exempt
import smtplib
from register.models import *
from email.mime.text import MIMEText
from django.contrib.auth.hashers import make_password
ver = ''
user = None
uname = ''
# Create your views here.
@csrf_exempt
def retrieve_views(request):
    return render(request, 'retrieve_00.html')

@csrf_exempt
def retrieve_01_views(request):
    print('用户存在，开始配置验证码')
    global ver, uname, user
    print('获取信息完毕')
    print(ver)
    print('旧的验证码是否清除')
    ver = ''
    while True:
        ver += str(random.randint(0, 9))
        if len(ver) == 6:
            break
    print('验证码生成完毕')
    mailto = uname
    mail_host = "smtp.qq.com"
    mail_user = "pandaweather"
    mail_pass = "lalfajxlfidzbhii"
    mail_postfix = "qq.com"
    print('邮箱账号及收件人准备就绪')
    nickname = (user.nickname)
    ver_msg = 'Hi,' + nickname + '!欢迎使用Panda Weather!您的密码找回验证码为' + ver
    print('验证码邮件就绪')
    def send_mail(to_list, sub, content):
        me = "Panda Weather" + "<" + mail_user + "@" + mail_postfix + ">"
        msg = MIMEText(content, _subtype='plain')
        msg['Subject'] = sub
        msg['From'] = me
        msg['To'] = mailto
        print('准备登录邮箱')
        server = smtplib.SMTP()
        server.connect(mail_host)
        server.login(mail_user, mail_pass)
        print('准备发送邮件')
        server.sendmail(me, to_list, msg.as_string())
        server.close()
        print('验证码已发送')
    send_mail(mailto, "Panda Weather找回密码", ver_msg)
    return render(request, 'retrieve_01.html', locals()) # 用户存在，验证码已发送

@csrf_exempt
def retrieve_02_views(request):
    global ver
    if ver == request.POST['verification']:
        return render(request, 'retrieve_02.html')
    else:
        return render(request, 'retrieve_05.html')

@csrf_exempt
def retrieve_03_views(request):
    print('服务器已接收到请求')
    print('开始检测用户是否存在')
    global user, uname
    uname = request.POST['uname']
    print('将信息发往数据库进行比对')
    try:
        user = User.objects.get(name=uname)
        print('比对完成')
    except:
        user = None
    if user:
        print('用户存在')
        return retrieve_01_views(request) # 用户存在，跳转到retrieve_01_views(request)
    else:
        print('用户不存在')
        return render(request, 'retrieve_03.html')  # 用户不存在，请确认您的邮箱地址填写无误 邮箱地址：口口口口口口 发送验证码

@csrf_exempt
def retrieve_04_views(request):
    newpwd = request.POST['newpwd']
    newpwd = make_password(newpwd, None, 'pbkdf2_sha256')
    user.pwd = newpwd
    user.save()
    return render(request, 'retrieve_04.html')