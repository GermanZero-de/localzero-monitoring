"use client";

import { useState } from "react";
import { db } from "./db/db.server";
import { cpmonitorCity } from "./db/schema";

export default function Search(props) {
  const [filteredCities, setFilteredCities] = useState([]);

  const search = (event) => {
    const searchTerm = event.target.value;

    const filteredCities = props.cities.filter((city) =>
      city.name.toLowerCase().startsWith(searchTerm.toLowerCase()),
    );
    setFilteredCities(filteredCities);
  };

  return (
    <>
      <div>Suche Kommune</div>
      <input type="text" placeholder="Name oder PLZ" onChange={search} />
      <ul>
        {filteredCities.map((city) => (
          <li key={city.name}>{city.name}</li>
        ))}
      </ul>
    </>
  );
}
