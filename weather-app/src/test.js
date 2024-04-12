import React from 'react';
import { render, waitFor, fireEvent, screen } from '@testing-library/react';
import App from './App';
import axios from 'axios';
import MockAdapter from 'axios-mock-adapter';

// Setup axios mock adapter
const mock = new MockAdapter(axios);

describe('Realistic fetchWeather Tests', () => {
  it('fetches sunny weather for Los Angeles', async () => {
    const city = "Los Angeles";
    const weatherData = { temp: 25, description: "Sunny" };
    mock.onGet(`http://127.0.0.1:5000/weather?city=${city}`).reply(200, weatherData);

    render(<App />);
    
    fireEvent.change(screen.getByPlaceholderText(/enter city name/i), { target: { value: city } });
    fireEvent.click(screen.getByText("Fetch Weather"));
    
    await waitFor(() => {
      expect(screen.getByText(/sunny/i)).toBeInTheDocument();
    });
  });

  it('fetches cloudy weather for London', async () => {
    const city = "London";
    const weatherData = { temp: 15, description: "Cloudy" };
    mock.onGet(`http://127.0.0.1:5000/weather?city=${city}`).reply(200, weatherData);

    render(<App />);

    fireEvent.change(screen.getByPlaceholderText(/enter city name/i), { target: { value: city } });
    fireEvent.submit(screen.getByRole('button', { name: /fetch weather/i }));

    await waitFor(() => {
      expect(screen.getByText(/cloudy/i)).toBeInTheDocument();
    });
  });
});
