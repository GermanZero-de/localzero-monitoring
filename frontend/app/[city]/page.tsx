"use client";

import { usePathname } from 'next/navigation';
import { Container } from "react-bootstrap";
import axios from "axios";
import { useState, useEffect } from 'react';
import Markdown from 'react-markdown'

export default function CityDashboard() {
  const [city, setCity] = useState({});

  const pathname = usePathname();
  const slug = pathname.split("/").at(-1)

  const getCity = async () => {
    const response = await axios.get("http://127.0.0.1:8000/api/cities/" + slug, { // TODO: proper url
      headers: {
        Accept: "application/json",
        "Content-Type": "application/json;charset=UTF-8",
      },
    }).then(response => {
      console.log(response.data);
      setCity(response.data);
    })
    .catch(error => {
      console.error('Error fetching data: ', error); // TODO: error handling
    });
  }

  useEffect(() => {getCity()}, []);

  if (!city.name) {
    return <></>;
  }

  return (
    <>
      <Container>
        <h1>{city.name.toUpperCase()}</h1>
        TODO Kacheln
        <p className="block-text pb-3">
        <Markdown children={city.description} />
        </p>
        <h2>Lokalteam {city.name}</h2>
        <p className="block-text pb-3">
          {city.name}
        </p>
        <h2>Mit Unterstützung von</h2>
        <p className="block-text pb-3">
          <Markdown children={city.supporting_ngos} />
        </p>
      </Container>
    </>
  );
}
