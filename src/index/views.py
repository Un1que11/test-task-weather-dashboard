from flask import Blueprint
from flask_restful import Api

from src.index.index import WeatherDashdoard
from src.index.autocomplete import Autocomplete
from src.index.search_history import History


index_bp = Blueprint("index", __name__)
api = Api(index_bp)

api.add_resource(WeatherDashdoard, "/")
api.add_resource(Autocomplete, "/autocomplete")
api.add_resource(History, "/history")
