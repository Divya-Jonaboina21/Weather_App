from django.shortcuts import render
from django.http import HttpResponse
from datetime import datetime,timezone,timedelta
import json

import requests



# Create your views here.
def index(request):
    if request.method == "POST":
        city=str(request.POST.get('city'))
        print(f"City from POST request :{city}")

        api_key ="0620889d52ee9d6f612f88b667bc0502"
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
        # data=requests.get(url).json()
        # print(f"API Response: {data}")

        try:
            data=requests.get(url).json()
            print(f"API Response: {data}")

            if data['cod']=='404':
                return render(request,'index.html',{'status':'notfound'})
            
            city_name=data['name']
            country=data.get('sys',{}).get('country','-')
            ts=data['dt']
            tzone=data['timezone']
            date_time=datetime.fromtimestamp(ts, tz=timezone(timedelta(seconds=tzone))).strftime('%Y-%m-%d')
            temp=int(data['main']['temp'])
            temp_F=format((temp*1.8)+32,'.1f')
            description=data['weather'][0]['icon']
            icon=data['weather'][0]['icon']
            humidity=data['main']['humidity']
            feels_like=int(data['main']['feels_like'])
            wind=format(data['wind']['speed']*3.6,'.1f')
            visibility=format(data['visibility']/1000,'.2f')
            context={
                'status':"success",
                'city':city_name,
                'country':country,
                'date_time':date_time,
                'temp':temp,
                'temp_F':temp_F,
                'description':description,
                'humidity':humidity,
                'feels_like':feels_like,
                'wind':wind,
                'visibility':visibility,
                'icon':icon
            }
            return render(request,'index.html',context)
        except Exception as e:
            print(f"error: {e}")
            return render(request,'index.html',{'status':'error'})
    return render(request, 'index.html',{'status':None})