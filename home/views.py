from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from weather.models import *
# Create your views here.
@csrf_exempt
def home_views(request):
    if request.method == 'GET':
        return render(request, 'home_00.html')
    else:
        msg = request.POST['city']
        msg = msg.split('-')
        city = msg[1]
        prov = msg[0]
        print(city, prov)
        infodic = Weather_now.objects.get(city=(prov+'-'+city))
        infotdic = Weather_tom.objects.get(city_id=prov+'-'+city)
        prov = None
        date = infodic.weat_now
        temp = infodic.temp_now
        humi = infodic.humi_now
        airq = infodic.airq_now
        wind = infodic.wind_now
        rays = infodic.rays_now
        print(rays)
        infodic = None
        ttomw = infotdic.weat_tom
        ttemp = infotdic.temp_tom
        tairq = infotdic.airq_tom
        twind = infotdic.wind_tom
        tdate = infotdic.date_tom
        infotdic = None
        return render(request, 'home_01.html', locals())

def test(request):
    return render(request, 'test.html')