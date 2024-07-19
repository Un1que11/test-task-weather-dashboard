import unittest

from src import create_app, db
from src.config import ConfigTest
from src.models import SearchHistory

class WeatherAppTestCase(unittest.TestCase):

    def setUp(self):
        self.app = create_app(ConfigTest)
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.client = self.app.test_client()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_homepage_loads(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Weather App', response.data)

    def test_get_weather(self):
        response = self.client.post('/', data=dict(city='London'))
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Temperature:', response.data)

    def test_autocomplete(self):
        # Add some search history for testing
        with self.app.app_context():
            history = SearchHistory(city_name='London', session_id='test_session')
            db.session.add(history)
            db.session.commit()
        
        response = self.client.get('/autocomplete?term=Lon')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'London', response.data)

    def test_search_history(self):
        # Add some search history for testing
        with self.app.app_context():
            history = SearchHistory(city_name='London', session_id='test_session', search_count=3)
            db.session.add(history)
            db.session.commit()

        response = self.client.get('/history')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'{}', response.data)
        self.assertIn(b'', response.data)

if __name__ == '__main__':
    unittest.main()
