import unittest
import json
from weather_server  import app

class WeatherAppTestCase(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()
        app.config['TESTING'] = True 

    def test_weather_endpoint_with_valid_city(self):
        response = self.client.get('/weather?city=London&unit=C')
        data = json.loads(response.data)
        
        self.assertEqual(response.status_code, 200)
        self.assertIn('Temperature', data)
        self.assertTrue('C' in data['Temperature'], "Temperature unit is not Celsius")

    def test_weather_endpoint_with_invalid_city(self):
        response = self.client.get('/weather?city=UnknownCity')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertIn('Error', data)

    def test_weather_by_coords_endpoint(self):
        response = self.client.get('/weather_by_coords?lat=51.5085&lon=-0.1257')
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertIn('coord', data)
        self.assertAlmostEqual(data['coord']['lat'], 51.5074, places=4)
        self.assertAlmostEqual(data['coord']['lon'], -0.1278, places=4)


    def test_forecast_endpoint_with_valid_city(self):
        response = self.client.get('/forecast?city=London&days=3')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertIn('city', data)
        self.assertEqual(data['city']['name'], 'London')
        self.assertTrue(len(data['forecast']) <= 3*8, "Forecast data exceeds expected length for 3 days")

    def test_forecast_endpoint_with_invalid_days(self):
        response = self.client.get('/forecast?city=London&days=6')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 400)
        self.assertIn('error', data)

if __name__ == '__main__':
    unittest.main()
