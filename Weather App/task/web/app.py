import sys
from os import environ
from requests import get
import json

from flask import Flask, render_template, request

app = Flask(__name__)
api_key = environ['OpenWeather_API_KEY']
weather = [{'card_class': 'night', 'degree': 9, 'state': 'Chilly', 'city': 'BOSTON'},
           {'card_class': 'day', 'degree': 32, 'state': 'Sunny', 'city': 'NEW YORK'},
           {'card_class': 'evening-morning', 'degree': -15, 'state': 'Cold', 'city': 'EDMONTON'}]


@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html', records=weather)


@app.route('/add', methods=['GET', 'POST'])
def add_city():
    city_name = request.form['city_name']
    response = get('http://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid={}'
                   .format(city_name, api_key))
    weather_raw = json.loads(response.content)
    city_weather = {'card_class': 'night', 'degree': weather_raw['main']['temp'],
                    'state': weather_raw['weather'][0]['description'], 'city': weather_raw['name']}
    weather.append(city_weather)
    return render_template('index.html', records=weather)


@app.route('/profile')
def profile():
    return 'This is profile page'


@app.route('/login')
def log_in():
    return 'This is login page'


# don't change the following way to run flask:
if __name__ == '__main__':
    if len(sys.argv) > 1:
        arg_host, arg_port = sys.argv[1].split(':')
        app.run(host=arg_host, port=arg_port)
    else:
        app.run()
