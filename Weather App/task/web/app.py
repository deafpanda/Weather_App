import os
import sys
from os import environ, path

from requests import get
import json

from flask import Flask, flash, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from cachetools import cached, TTLCache

app = Flask(__name__)

app.config['SECRET_KEY'] = os.urandom(64)
app.config['DEBUG'] = True

basedir = path.abspath(path.dirname(__file__))
sqldb_filename = 'weather.db'

# Setup SQLAlchemy Environment
app.config['SQLALCHEMY_DATABASE_URI'] = \
    'sqlite:///' + path.join(basedir, sqldb_filename)

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

db = SQLAlchemy(app)


class City(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)


with app.app_context():
    try:
        db.create_all()
        print("Created " + sqldb_filename + " SQLLite Database")
    except Exception as exception:
        print("got the following exception when attempting db.create_all(): " + str(exception))
    finally:
        print("db.create_all() was successful - no exceptions were raised")

api_key = environ['OpenWeather_API_KEY']
weather = []


@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html', records=weather)


# cache weather data for no longer than ten minutes
@cached(cache=TTLCache(maxsize=1024, ttl=600))
@app.route('/add', methods=['GET', 'POST'])
def add_city():
    city_name = request.form['city_name']
    response = get('http://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid={}'
                   .format(city_name, api_key))
    if response.ok:
        weather_raw = json.loads(response.content)
        card_class = 'day' if weather_raw['sys']['sunset'] > weather_raw['dt'] > weather_raw['sys'][
            'sunrise'] else 'night'
        city_weather = {'card_class': card_class, 'id': weather_raw['id'], 'degree': weather_raw['main']['temp'],
                        'state': weather_raw['weather'][0]['description'], 'city': weather_raw['name']}

        city = City()
        __tablename__ = "city"
        city.id = weather_raw['id']
        city.name = weather_raw['name']

        try:
            db.session.add(city)
            db.session.commit()
            weather.append(city_weather)
        except Exception as exception:
            flash(f'The city has already been added to the list!', 'error')
            # print("got the following exception when attempting db.create_all(): " + str(exception))
        finally:
            print(f"City, {city_name} added successfully- no exceptions were raised")

    else:
        flash(f'The city doesn\'t exist!', 'error')
    return render_template('index.html', records=weather)


@app.route('/delete', methods=['GET', 'POST'])
def delete_city():
    city_id = request.form['id']
    city = City.query.filter_by(id=city_id).first()
    db.session.delete(city)
    db.session.commit()
    weather.remove(next(item for item in weather if item["id"] == int(city_id)))
    return redirect('/')

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
