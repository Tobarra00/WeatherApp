import os
import datetime
import requests
from dotenv import load_dotenv

from django.shortcuts import render

load_dotenv() # loading api key

# Create your views here.

def index(request):
    
    API_KEY = os.environ['API_KEY']
    
    if request.method == 'POST':
        user_input = request.POST['city']
        city_location = 'https://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid={}'
        forecast_city = 'https://api.openweathermap.org/data/2.5/forecast?lat={}&lon={}&units=metric&appid={}'
        
        city_weather, city_forecast = forecast_weather(user_input, city_location, forecast_city, API_KEY)
        
        context = {
            'city_weather': city_weather,
            'city_forecast': city_forecast
        }
        return render(request, 'base.html', context)
    else:
        return render(request, 'base.html')
    
def forecast_weather(user_input, city_location, forecast_city, API_KEY):

    city_weather_response = requests.get(city_location.format(user_input, API_KEY)).json()
    if city_weather_response['cod'] != 200:
        return None, None
    latitude, longitude = city_weather_response['coord']['lat'], city_weather_response['coord']['lon']
    forecast_city = requests.get(forecast_city.format(latitude, longitude, API_KEY)).json()
    complete_forecast_city = []
    for forecast in forecast_city['list']:
        if '15:00:00' in forecast['dt_txt']:
            complete_forecast_city.append({
                'city': city_weather_response['name'],
                'date': datetime.datetime.utcfromtimestamp(forecast['dt']).strftime('%A %Y-%m-%d'),
                'temp': forecast['main']['temp'],
                'temp_min': forecast['main']['temp_min'],
                'temp_max': forecast['main']['temp_max'],
                'weather': forecast['weather'][0]['main'],
                'icon': forecast['weather'][0]['icon'],
                })
    
    today_weather = {
        'city': city_weather_response['name'],
        'date': datetime.datetime.utcfromtimestamp(city_weather_response['dt']).strftime('%A %Y-%m-%d'),
        'temp': city_weather_response['main']['temp'],
        'temp_min': city_weather_response['main']['temp_min'],
        'temp_max': city_weather_response['main']['temp_max'],
        'weather': city_weather_response['weather'][0]['main'],
        'icon': city_weather_response['weather'][0]['icon'],        
    }
    
    return today_weather, complete_forecast_city
    