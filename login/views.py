from django.shortcuts import render
from register.models import *
from home.views import *
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.hashers import check_password
from weather.views import *
# Create your views here.
@csrf_exempt
def login_views(request):
    if request.method == 'GET':
        return render(request, 'login_00.html')
    elif request.method == 'POST':
        print('\n' * 3)
        print(request.POST)
        print('\n' * 3)
        # 非登录的情况
        if 'upwd' not in request.POST:
            # 查询某城市天气
            if 'city' in request.POST:
                return city_search(request)
            # 点击修改常用城市按钮
            elif 'configure' in request.POST:
                uname = request.POST['uname'][3:]
                user = User.objects.get(name=uname)
                city1 = user.city1
                city2 = user.city2
                city3 = user.city3
                return render(request, 'configure_00.html', locals())
            # 修改常用城市完成点击确认按钮
            elif 'usualcity' in request.POST:
                usualcity = request.POST['usualcity']
                uname = request.POST['uname'][3:]
                radiocity = request.POST['radiocity']
                user = User.objects.get(name=uname)
                if radiocity == '1':
                    user.city1 = usualcity
                elif radiocity == '2':
                    user.city2 = usualcity
                else:
                    user.city3 = usualcity
                user.save()
                return get_databases(request, user, uname)
            # 修改是否接收天气提醒
            uname = request.POST['uname'][3:]
            accept = request.POST['accept']
            user = User.objects.get(name=uname)
            if accept == '不再接收天气提醒':
                user.accept = 2
                user.save()
                return get_databases(request, user, uname)
            else:
                user.accept = 1
                user.save()
                return get_databases(request, user, uname)
        # 登录的情况
        uname = request.POST['uname']
        upwd = request.POST['upwd']
        user = User.objects.filter(name__exact=uname)
        # 如果用户名存在
        if user:
            user = User.objects.get(name=uname)
            # 如果密码正确
            if check_password(upwd, user.pwd):
                upwd = None
                return get_databases(request, user, uname)
            # 如果密码不正确
            user = None
            return render(request, 'login_01.html', locals())
        # 如果用户名不存在
        print('无此用户')
        return render(request, 'login_02.html', locals())

def get_databases(request, user, uname):
    accept = user.accept
    print(accept)
    if accept == 1:
        accept = '不再接收天气提醒'
    else:
        accept = '开始接收天气提醒'
    city1 = user.city1
    if '默认:' in city1:
        city1 = city1[3:]
    city2 = user.city2
    if '默认:' in city2:
        city2 = city2[3:]
    city3 = user.city3
    if '默认:' in city3:
        city3 = city3[3:]
    user = None
    weather = Weather_now.objects.get(city=city1)
    weathert = Weather_tom.objects.get(city_id=city1)
    city1 = city1.split('-')[1]
    time1 = weather.time_now
    date1 = weather.weat_now
    temp1 = weather.temp_now
    humi1 = weather.humi_now
    airq1 = weather.airq_now
    rays1 = weather.rays_now
    wind1 = weather.wind_now
    tdate1 = weathert.date_tom
    ttomw1 = weathert.weat_tom
    ttemp1 = weathert.temp_tom
    tairq1 = weathert.airq_tom
    twind1 = weathert.wind_tom
    weather = Weather_now.objects.get(city=city2)
    weathert = Weather_tom.objects.get(city_id=city2)
    city2 = city2.split('-')[1]
    time2 = weather.time_now
    date2 = weather.weat_now
    temp2 = weather.temp_now
    humi2 = weather.humi_now
    airq2 = weather.airq_now
    rays2 = weather.rays_now
    wind2 = weather.wind_now
    tdate2 = weathert.date_tom
    ttomw2 = weathert.weat_tom
    ttemp2 = weathert.temp_tom
    tairq2 = weathert.airq_tom
    twind2 = weathert.wind_tom
    weather = Weather_now.objects.get(city=city3)
    weathert = Weather_tom.objects.get(city_id=city3)
    city3 = city3.split('-')[1]
    time3 = weather.time_now
    date3 = weather.weat_now
    temp3 = weather.temp_now
    humi3 = weather.humi_now
    airq3 = weather.airq_now
    rays3 = weather.rays_now
    wind3 = weather.wind_now
    tdate3 = weathert.date_tom
    ttomw3 = weathert.weat_tom
    ttemp3 = weathert.temp_tom
    tairq3 = weathert.airq_tom
    twind3 = weathert.wind_tom
    weather = None
    weathert = None
    return render(request, 'weather_00.html', locals())

def city_search(request):
    uname = request.POST['uname'][3:]
    accept = request.POST['accept']
    prov = request.POST['city'].split('-')[0]
    city = request.POST['city'].split('-')[1]
    infodic = Weather_now.objects.get(city=(prov + '-' + city))
    infotdic = Weather_tom.objects.get(city_id=prov + '-' + city)
    prov = None
    time = infodic.time_now
    date = infodic.weat_now
    temp = infodic.temp_now
    humi = infodic.humi_now
    airq = infodic.airq_now
    wind = infodic.wind_now
    rays = infodic.rays_now
    infodic = None
    ttomw = infotdic.weat_tom
    ttemp = infotdic.temp_tom
    tairq = infotdic.airq_tom
    twind = infotdic.wind_tom
    tdate = infotdic.date_tom
    infotdic = None
    user = User.objects.get(name=uname)
    accept = user.accept
    print(accept)
    if accept == 1:
        accept = '不再接收天气提醒'
    else:
        accept = '开始接收天气提醒'
    city1 = user.city1
    if '默认:' in city1:
        city1 = city1[3:]
    city2 = user.city2
    if '默认:' in city2:
        city2 = city2[3:]
    city3 = user.city3
    if '默认:' in city3:
        city3 = city3[3:]
    user = None
    weather = Weather_now.objects.get(city=city1)
    weathert = Weather_tom.objects.get(city_id=city1)
    city1 = city1.split('-')[1]
    time1 = weather.time_now
    date1 = weather.weat_now
    temp1 = weather.temp_now
    humi1 = weather.humi_now
    airq1 = weather.airq_now
    rays1 = weather.rays_now
    wind1 = weather.wind_now
    tdate1 = weathert.date_tom
    ttomw1 = weathert.weat_tom
    ttemp1 = weathert.temp_tom
    tairq1 = weathert.airq_tom
    twind1 = weathert.wind_tom
    weather = Weather_now.objects.get(city=city2)
    weathert = Weather_tom.objects.get(city_id=city2)
    city2 = city2.split('-')[1]
    time2 = weather.time_now
    date2 = weather.weat_now
    temp2 = weather.temp_now
    humi2 = weather.humi_now
    airq2 = weather.airq_now
    rays2 = weather.rays_now
    wind2 = weather.wind_now
    tdate2 = weathert.date_tom
    ttomw2 = weathert.weat_tom
    ttemp2 = weathert.temp_tom
    tairq2 = weathert.airq_tom
    twind2 = weathert.wind_tom
    weather = Weather_now.objects.get(city=city3)
    weathert = Weather_tom.objects.get(city_id=city3)
    city3 = city3.split('-')[1]
    time3 = weather.time_now
    date3 = weather.weat_now
    temp3 = weather.temp_now
    humi3 = weather.humi_now
    airq3 = weather.airq_now
    rays3 = weather.rays_now
    wind3 = weather.wind_now
    tdate3 = weathert.date_tom
    ttomw3 = weathert.weat_tom
    ttemp3 = weathert.temp_tom
    tairq3 = weathert.airq_tom
    twind3 = weathert.wind_tom
    weather = None
    weathert = None
    return render(request, 'weather_01.html', locals())