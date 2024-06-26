import { useState, FormEvent } from "react";
import axios from "axios";
import "./index.css";

interface WeatherData {
  Temperature?: string;
  Humidity?: string;
  Description?: string;
  Error?: string;
}

function App() {
  const [city, setCity] = useState<string>("");
  const [days, setDays] = useState<number>(1);
  const [latitude, setLatitude] = useState<string>("");
  const [longitude, setLongitude] = useState<string>("");
  const [weather, setWeather] = useState<WeatherData | null>(null);
  const [fetchType, setFetchType] = useState<
    "current" | "coordinates" | "forecast"
  >("current");

  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault();
    fetchWeather();
  };

  const fetchWeather = async () => {
    let url = `http://127.0.0.1:5000/weather?city=${city}`;

    switch (fetchType) {
      case "coordinates":
        url = `http://localhost:5000/weather_by_coords?lat=${latitude}&lon=${longitude}`;
        break;
      case "forecast":
        url = `http://localhost:5000/forecast?city=${city}&days=${days}`;
        break;
    }

    try {
      const response = await axios.get<WeatherData>(url);
      setWeather(response.data);
    } catch (error) {
      setWeather({ Error: "Failed to fetch weather data" });
    }
  };

  const renderFormInputs = () => {
    switch (fetchType) {
      case "forecast":
        return (
          <>
            <input
              type="number"
              min="1"
              max="5"
              value={days}
              onChange={(e) => setDays(Number(e.target.value))}
              placeholder="Enter number of days"
              className="input input-bordered w-full max-w-xs"
            />
            <input
              type="text"
              value={city}
              onChange={(e) => setCity(e.target.value)}
              placeholder="Enter city name"
              className="input input-bordered w-full max-w-xs"
            />
          </>
        );
      case "coordinates":
        return (
          <>
            <input
              type="text"
              value={latitude}
              onChange={(e) => setLatitude(e.target.value)}
              placeholder="Enter latitude"
              className="input input-bordered w-full max-w-xs"
            />
            <input
              type="text"
              value={longitude}
              onChange={(e) => setLongitude(e.target.value)}
              placeholder="Enter longitude"
              className="input input-bordered w-full max-w-xs"
            />
          </>
        );
      default:
        return (
          <input
            type="text"
            value={city}
            onChange={(e) => setCity(e.target.value)}
            placeholder="Enter city name"
            className="input input-bordered w-full max-w-xs"
          />
        );
    }
  };
  const renderOutputUI = () => {
    if (!weather) {
      return <p>Loading weather data...</p>;  
    }
  
    switch (fetchType) {
      case "current":
        if (!weather) {
   
          return <p>Weather data not available.</p>;
        }
        return (
          <div>
            <h3>Current Weather</h3>
            <div>
              <p>Temperature: {weather.weather.feels_like}</p>
              <p>Place: {weather.name}</p>
              <p>Humidity: {weather.weather.humidity}</p>
            </div>
          </div>
        );
      case "coordinates":
        console.log(weather)

      if (!weather) {
        return <p>Weather data not available.</p>;
      }
        return (
          <div className="w-full bg-black min-h-screen flex justify-center items-center">
            <div className="bg-gray-800 text-white p-8 rounded-lg shadow-md max-w-2xl w-full">
              <h3 className="text-blue-300 text-2xl font-semibold mb-4">
                Weather Details
              </h3>
              <div>
              <p>Temperature: {((weather.main.feels_like - 273.15) ).toFixed(2)}°C</p>
              <p>Place: {weather.name}</p>
              <p>Humidity: {weather.main.humidity}</p>
              </div>
            </div>
          </div>
        );
      case "forecast":
        if (!weather.forecast) {
          return <p>Forecast data not available.</p>;
        }
        return (
          <div className="w-full bg-black min-h-screen flex justify-center items-center">
            <div className="bg-gray-800 text-white p-8 rounded-lg shadow-lg max-w-4xl">
              <h3 className="text-blue-300 text-2xl font-semibold mb-4">
                Weather Forecast
              </h3>
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                {weather.forecast.map((item, index) => (
                  <div key={index} className="bg-gray-700 p-4 rounded-lg">
                    <p className="font-bold">{new Date(item.dt * 1000).toLocaleString()}</p>
                    <p>Weather: {item.weather[0].main} - {item.weather[0].description}</p>
                    <p>Temperature: {(item.main.temp - 273.15).toFixed(2)}°C</p>
                    <p>Humidity: {item.main.humidity}%</p>
                  </div>
                ))}
              </div>
            </div>
          </div>
        );
      default:
        return null;
    }
  };
  

  return (
    <div className="w-full bg-black min-h-screen flex justify-center items-center">
      <header className="bg-gray-800 text-white p-8 rounded-lg shadow-md w-full max-w-4xl">
        <h2 className="text-blue-300 text-3xl font-semibold mb-6">
          Weather App
        </h2>
        <form
          onSubmit={handleSubmit}
          className="flex flex-col text-black gap-4"
        >
          {renderFormInputs()}
          <select
            value={fetchType}
            onChange={(e) => setFetchType(e.target.value)}
            className="select select-bordered w-full max-w-xs"
          >
            <option value="current">Current Weather</option>
            <option value="coordinates">Weather by Coordinates</option>
            <option value="forecast">Weather Forecast</option>
          </select>
          <button
            type="submit"
            className="btn btn-blue-500 w-full max-w-xs text-white"
          >
            Get Weather
          </button>
        </form>
        <div className="mt-6 bg-white text-black p-4 rounded-lg">
          {renderOutputUI()}
        </div>
      </header>
    </div>
  );
}

export default App;
