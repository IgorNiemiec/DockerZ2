import React from 'react';

export default function WeatherDisplay({ data }) {
  if (!data) return null;
  const { current, hourly, daily } = data;
  return (
    <div className="space-y-6 mt-6">
      <section className="p-4 border rounded">
        <h2 className="text-xl font-semibold mb-2">Pogoda bieżąca</h2>
        <p>Temperatura: {current.temperature ?? current.temp} °C</p>
        <p>Opis: {current.conditions ?? current.weather?.[0]?.description}</p>
      </section>
      {/* Możesz rozszerzyć wyświetlanie prognoz hourly i daily tutaj */}
    </div>
  );
}