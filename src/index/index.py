import requests
from flask import render_template, request, session, make_response, current_app
from flask_restful import Resource

import uuid

from src import db
from src.models import SearchHistory

X_API_KEY = current_app.config["X_API_KEY"]


class WeatherDashdoard(Resource):

    def __init__(self):
        self.search_history = SearchHistory
        self.db = db

    def get(self):
        weather_data = None
        return make_response(render_template('index.html', weather=weather_data, city=session.get('city')))

    def post(self):
        if 'session_id' not in session:
            session['session_id'] = str(uuid.uuid4())

        weather_data = None
        session_id = session['session_id']
        last_city = session.get('city')

        city = request.form['city']
        session['city'] = city
        
        history = self.search_history.query.filter_by(city_name=city, session_id=session_id).first()
        if history:
            history.search_count += 1
        else:
            history = self.search_history(city_name=city, session_id=session_id)
            db.session.add(history)
        db.session.commit()

        lat, lon = self.get_city_coordinates(city)
        weather_data = self.get_weather(lat, lon)
        
        return make_response(render_template('index.html', weather=weather_data, city=last_city))

    @staticmethod
    def get_weather(lat, lon):
        api_url = f'https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&hourly=temperature_2m'
        response = requests.get(api_url)
        return response.json()
    
    @staticmethod
    def get_city_coordinates(city):
        api_url = f'https://api.api-ninjas.com/v1/geocoding?city={city}'
        response = requests.get(api_url, headers={"X-Api-Key": X_API_KEY})
        first_city = response.json()[0]
        lat, lon = first_city.get("latitude", 0.0), first_city.get("longitude", 0.0)
        return lat, lon
