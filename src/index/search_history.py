from flask_restful import Resource
from flask import jsonify, session

from src.models import SearchHistory


class History(Resource):

    def __init__(self):
        self.search_history = SearchHistory

    def get(self):
        session_id = session.get('session_id')
        if not session_id:
            return jsonify({})

        history = self.search_history.query.filter_by(session_id=session_id).all()
        results = {city.city_name: city.search_count for city in history}
        return jsonify(results)
    