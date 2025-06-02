import React from 'react';

export default function CountrySelector({ countries, onSelect }) {
  return (
    <select
      onChange={e => onSelect(e.target.value)}
      className="border p-2 rounded w-full"
    >
      <option value="">-- Wybierz kraj --</option>
      {countries.map(c => (
        <option key={c.iso2} value={c.iso2}>{c.name}</option>
      ))}
    </select>
  );
}