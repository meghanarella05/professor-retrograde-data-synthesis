import React from 'react';

type PlanetPosition = {
  name: string;
  sign: string;
};

type NorthIndianChartProps = {
  ascendantSign: string;
  planets: PlanetPosition[];
};

export function NorthIndianChart({ ascendantSign, planets }: NorthIndianChartProps) {
  return (
    <section>
      <h3>North Indian Chart</h3>
      <p>Ascendant: {ascendantSign}</p>
      <ul>
        {planets.map((planet) => (
          <li key={planet.name}>
            {planet.name}: {planet.sign}
          </li>
        ))}
      </ul>
    </section>
  );
}
