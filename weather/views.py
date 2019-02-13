from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
# Create your views here.
@login_required
@csrf_exempt
def weather_00_views(request):
    uname = request.POST['uname']
    print(uname)
    return render(request, 'weather_00.html')
