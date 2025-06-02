import axios from 'axios';

const API_BASE = process.env.REACT_APP_API_BASE;

export const fetchCountries = () =>
  axios.get(`${API_BASE}/countries`).then(res => res.data);

export const fetchCities = countryCode =>
  axios.get(`${API_BASE}/countries/${countryCode}/cities`).then(res => res.data);

export const fetchWeather = (countryCode, city) =>
  axios
    .get(`${API_BASE}/weather`, { params: { country_code: countryCode, city } })
    .then(res => res.data);