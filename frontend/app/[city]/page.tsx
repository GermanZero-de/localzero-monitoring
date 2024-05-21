"use client";

import { usePathname } from 'next/navigation';
import { Container } from "react-bootstrap";
import axios from "axios";
import { useState, useEffect } from 'react';
import Markdown from 'react-markdown';
import Image from "next/image";
import arrow from "../../public/images/arrow-right-down.svg";
import LocalGroup from '../components/LocalGroup';

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
        <h1 style={{fontWeight: 600,fontSize: 38}}>{city.name.toUpperCase()}<Image src={arrow} alt="" /></h1>
        TODO Kacheln
        <Markdown className="block-text pb-3" children={city.description} />
      </Container>
      <div className="backgroundColor">
        <Container>
        <LocalGroup local_group={city.local_group}/>
        <h2>Mit Unterstützung von</h2>
        <Markdown className="block-text pb-3" children={city.supporting_ngos} />
        </Container>
      </div>
    </>
  );
}
