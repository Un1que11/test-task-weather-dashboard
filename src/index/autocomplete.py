from flask_restful import Resource
from flask import render_template, request, session, jsonify

from src.models import SearchHistory


class Autocomplete(Resource):

    def __init__(self):
        self.search_history = SearchHistory

    def get(self):
        search = request.args.get('term')
        cities = self.search_history.query.filter(self.search_history.city_name.like(f'%{search}%')).all()
        results = [city.city_name for city in cities]
        return jsonify(results)
    