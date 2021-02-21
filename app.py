from flask import Flask, request, render_template, url_for
from markupsafe import escape
import requests
import time
import os

app = Flask(__name__)

WEATHER_API_KEY = os.getenv('WEATHER_API_KEY')

def calculateLocalTime(timezone):
    gmtTime = time.time()
    localTime = time.gmtime(gmtTime + timezone)
    return time.strftime("%H:%M", localTime)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/weather')
def weather():
    weather_api = "http://api.openweathermap.org/data/2.5/weather"
    search_location = request.args.get('location')
    response = requests.get(weather_api, params={"q":search_location, "appid":WEATHER_API_KEY, "units":"metric"})
    if response.status_code == 200:
        timezone = response.json().get("timezone")
        return render_template('weather.html', data=response.json(), localTime=calculateLocalTime(timezone))
    elif response.status_code == 404:
        return "Location Not Found."
    else:
        return str(response.text)
