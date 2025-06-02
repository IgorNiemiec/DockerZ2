import React from 'react';

export default function CitySelector({ cities, onSelect }) {
  return (
    <select
      onChange={e => onSelect(e.target.value)}
      className="border p-2 rounded w-full"
      disabled={!cities.length}
    >
      <option value="">-- Wybierz miasto --</option>
      {cities.map(name => (
        <option key={name} value={name}>{name}</option>
      ))}
    </select>
  );
}