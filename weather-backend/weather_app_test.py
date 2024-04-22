import json
import pytest
from unittest.mock import patch  
from weather_server import app

@pytest.fixture
def client():
    """Nastaví testovacího klienta pro aplikaci."""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_weather_endpoint_with_valid_city(client):
    """Otestuje, zda endpoint `/weather` vrátí správné údaje pro platné město."""
    response = client.get('/weather?city=London&unit=C')
    data = json.loads(response.data)
    assert response.status_code == 200
    assert 'Temperature' in data
    assert 'C' in data['Temperature'], "Jednotka teploty není ve stupních Celsia"

def test_weather_endpoint_with_invalid_city(client):
    """Otestuje, zda endpoint `/weather` vrátí chybovou zprávu pro neplatné město."""
    response = client.get('/weather?city=UnknownCity')
    data = json.loads(response.data)
    assert response.status_code == 200
    assert 'Error' in data

def test_weather_by_coords_endpoint(client):
    """Otestuje, zda endpoint `/weather_by_coords` správně vrací data podle zeměpisných souřadnic."""
    response = client.get('/weather_by_coords?lat=51.5085&lon=-0.1257')
    data = json.loads(response.data)
    assert response.status_code == 200
    assert 'coord' in data
    assert abs(data['coord']['lat'] - 51.5074) < 0.0001
    assert abs(data['coord']['lon'] + 0.1278) < 0.0001

def test_forecast_endpoint_with_valid_city(client):
    """Otestuje, zda endpoint `/forecast` vrací předpověď počasí pro platné město."""
    response = client.get('/forecast?city=London&days=3')
    data = json.loads(response.data)
    assert response.status_code == 200
    assert 'city' in data
    assert data['city']['name'] == 'London'
    assert len(data['forecast']) <= 3 * 8, "Počet datových bodů předpovědi překračuje očekávanou délku pro 3 dny"

def test_forecast_endpoint_with_invalid_days(client):
    """Otestuje, zda endpoint `/forecast` vrátí chybu pro neplatný počet dní."""
    response = client.get('/forecast?city=London&days=6')
    data = json.loads(response.data)
    assert response.status_code == 400
    assert 'error' in data

def test_missing_city_parameter(client):
    """Otestuje, zda endpoint `/weather` správně ošetřuje chybějící parametr města."""
    response = client.get('/weather')
    data = json.loads(response.data)
    assert response.status_code == 400
    assert 'error' in data, "Chybí očekávaná chybová zpráva o absenci parametru města."

def test_temperature_unit_conversion(client):
    """Otestuje, zda je teplota správně převedena z Kelvinů na Celsia."""
    with patch('requests.get') as mock_get:
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {
            "main": {"temp": 282.15},  # 9 °C
            "weather": [{"description": "clear sky"}],
            "cod": 200
        }
        response = client.get('/weather?city=London&unit=C')
        data = json.loads(response.data)
        temperature = float(data['Temperature'].split()[0])
        assert temperature == pytest.approx(9.0, 0.01), "Teplota není správně převedena na stupně Celsia."


def test_response_format(client):
    """Ověří, zda formát odpovědi obsahuje všechny očekávané klíče."""
    response = client.get('/weather?city=London')
    data = json.loads(response.data)
    expected_keys = ['Temperature', 'Atmospheric Pressure', 'Humidity', 'Description']
    assert all(key in data for key in expected_keys), "Odpověď neobsahuje všechny očekávané klíče."
