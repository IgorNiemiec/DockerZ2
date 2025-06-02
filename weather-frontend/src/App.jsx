import React, { useEffect, useState } from 'react';
import { fetchCountries, fetchCities, fetchWeather } from './api';
import CountrySelector from './components/CountrySelector';
import CitySelector from './components/CitySelector';
import WeatherDisplay from './components/WeatherDisplay';

export default function App() {
  const [countries, setCountries] = useState([]);
  const [selectedCountry, setSelectedCountry] = useState('');
  const [cities, setCities] = useState([]);
  const [selectedCity, setSelectedCity] = useState('');
  const [weather, setWeather] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  useEffect(() => {
    fetchCountries()
      .then(setCountries)
      .catch(() => setError('Błąd ładowania krajów'));
  }, []);

  useEffect(() => {
    if (!selectedCountry) return;
    fetchCities(selectedCountry)
      .then(setCities)
      .catch(() => setError('Błąd ładowania miast'));
  }, [selectedCountry]);

  const handleSubmit = async e => {
    e.preventDefault();
    if (!selectedCountry || !selectedCity) return;
    setLoading(true);
    setError('');
    try {
      const data = await fetchWeather(selectedCountry, selectedCity);
      setWeather(data);
    } catch {
      setError('Nie udało się pobrać pogody');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-md mx-auto p-4">
      <h1 className="text-2xl font-bold mb-4">Aplikacja pogodowa</h1>
      <form onSubmit={handleSubmit} className="space-y-4">
        <CountrySelector countries={countries} onSelect={setSelectedCountry} />
        <CitySelector cities={cities} onSelect={setSelectedCity} />
        <button
          type="submit"
          className="bg-blue-500 text-white px-4 py-2 rounded"
          disabled={loading}
        >
          {loading ? 'Ładowanie...' : 'Pobierz pogodę'}
        </button>
      </form>
      {error && <p className="text-red-500 mt-4">{error}</p>}
      <WeatherDisplay data={weather} />
    </div>
  );
}