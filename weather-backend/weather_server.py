from flask import Flask, jsonify, request
import requests
from flask_cors import CORS
app = Flask(__name__)
CORS(app)  

def get_weather(api_key, city):
    base_url = "http://api.openweathermap.org/data/2.5/weather?"
    complete_url = f"{base_url}appid={api_key}&q={city}"
    response = requests.get(complete_url)
    weather_data = response.json()

    if weather_data.get("cod") == 200:  
        main_data = weather_data.get("main", {})
        current_temperature = main_data.get("temp", "Unavailable")
        current_pressure = main_data.get("pressure", "Unavailable")
        current_humidity = main_data.get("humidity", "Unavailable")
        weather_description = weather_data.get("weather", [{}])[0].get("description", "Unavailable")
        
        return {
            "Temperature": f"{current_temperature} Kelvin",
            "Atmospheric Pressure": f"{current_pressure} hPa",
            "Humidity": f"{current_humidity}%",
            "Description": weather_description.capitalize()
        }
    else:
        return {"Error": "City not found"}

def convert_temperature(kelvin, unit):
    """Convert temperature from Kelvin to Celsius or Fahrenheit."""
    if unit == 'C':
        return kelvin - 273.15
    elif unit == 'F':
        return kelvin * 9/5 - 459.67
    else:
        return kelvin

@app.route('/weather', methods=['GET'])
def weather():
    """Endpoint to get weather by city name with optional temperature unit conversion."""
    city = request.args.get('city')
    unit = request.args.get('unit', 'K')
    api_key = 'b19b9f3943e89c6e025fcbf777476da2'   
    if not city:
        return jsonify({'error': 'Missing city parameter'}), 400

    weather_info = get_weather(api_key, city)
    if 'Temperature' in weather_info:
        kelvin_temp = float(weather_info['Temperature'].split()[0])
        weather_info['Temperature'] = f"{convert_temperature(kelvin_temp, unit)} {unit}"
    return jsonify(weather_info)

@app.route('/weather_by_coords', methods=['GET'])
def weather_by_coords():
    """Endpoint to get weather by geographic coordinates."""
    latitude = request.args.get('lat')
    longitude = request.args.get('lon')
    api_key = 'b19b9f3943e89c6e025fcbf777476da2'   
    if not latitude or not longitude:
        return jsonify({'error': 'Missing latitude or longitude parameter'}), 400

    base_url = "http://api.openweathermap.org/data/2.5/weather?"
    complete_url = f"{base_url}appid={api_key}&lat={latitude}&lon={longitude}"
    response = requests.get(complete_url)
    return jsonify(response.json())


@app.route('/forecast', methods=['GET'])
def forecast():
    """Endpoint to get an extended weather forecast for a city with the option to specify the number of days."""
    city = request.args.get('city')
    days = request.args.get('days', default=5, type=int) 
    api_key = 'b19b9f3943e89c6e025fcbf777476da2'   

    if not city:
        return jsonify({'error': 'Missing city parameter'}), 400

    if days > 5:
        return jsonify({'error': 'Maximum forecast length is 5 days'}), 400

    base_url = "http://api.openweathermap.org/data/2.5/forecast?"
    complete_url = f"{base_url}appid={api_key}&q={city}"

    response = requests.get(complete_url)
    if response.status_code != 200:
        return jsonify({'error': 'Failed to fetch forecast data'}), response.status_code

    forecast_data = response.json()
    total_data_points = days * 8  

    filtered_forecast_data = forecast_data['list'][:total_data_points]


    return jsonify({
        'city': forecast_data['city'],
        'country': forecast_data['city']['country'],
        'forecast': filtered_forecast_data
    })


if __name__ == '__main__':
    app.run(debug=True)
