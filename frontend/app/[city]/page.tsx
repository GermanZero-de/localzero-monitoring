"use client";

import { usePathname } from "next/navigation";
import { Container } from "react-bootstrap";
import axios from "axios";
import { useState, useEffect } from "react";
import Markdown from "react-markdown";
import Image from "next/image";
import arrow from "../../public/images/arrow-right-down.svg";
import LocalGroup from "../components/LocalGroup";

const CityDescription = ({ description }) => {
  if (!description) {
    return <></>;
  }
  return (
    <>
      <h2>Klimaschutz in München</h2>
      <Markdown className="block-text pb-3">{description}</Markdown>
      <Markdown className="block-text pb-3">{description}</Markdown>
      <Markdown className="block-text pb-3">{description}</Markdown>
      <Markdown className="block-text pb-3">{description}</Markdown>
      <Markdown className="block-text pb-3">{description}</Markdown>
      <Markdown className="block-text pb-3">{description}</Markdown>
      <Markdown className="block-text pb-3">{description}</Markdown>
      <Markdown className="block-text pb-3">{description}</Markdown>
      <Markdown className="block-text pb-3">{description}</Markdown>
      <Markdown className="block-text pb-3">{description}</Markdown>
      <Markdown className="block-text pb-3">{description}</Markdown>
      <Markdown className="block-text pb-3">{description}</Markdown>
      <Markdown className="block-text pb-3">{description}</Markdown>
      <Markdown className="block-text pb-3">{description}</Markdown>
      <Markdown className="block-text pb-3">{description}</Markdown>
    </>
  );
};

const SupportingNgos = ({ supportingNgos }) => {
  if (!supportingNgos) {
    return <></>;
  }
  return (
    <>
      <h2>Mit Unterstützung von</h2>
      <Markdown className="block-text pb-3">{supportingNgos}</Markdown>
    </>
  );
};

export default function CityDashboard() {
  const [city, setCity] = useState({});
  const [hasError, setHasError] = useState(false);

  const pathname = usePathname();
  const slug = pathname.split("/").at(-1);

  const getCity = async () => {
    const response = await axios
      .get("http://127.0.0.1:8000/api/cities/" + slug, {
        // TODO: proper url
        headers: {
          Accept: "application/json",
          "Content-Type": "application/json;charset=UTF-8",
        },
      })
      .then((response) => {
        setCity(response.data);
      })
      .catch((error) => {
        setHasError(true);
        console.error("Error get city request: ", error);
      });
  };

  useEffect(() => {
    getCity();
  }, []);

  if (hasError) {
    return <h3 className="pb-3 pt-3">Für die Stadt {slug} gibt es kein Monitoring</h3>;
  }

  if (!city.name) {
    return <></>;
  }

  return (
    <>
      <Container>
        <h1 style={{ fontWeight: 600, fontSize: 38 }}>
          {city.name.toUpperCase()}
          <Image
            src={arrow}
            alt=""
          />
        </h1>
        <p className="pb-3">TODO Kacheln</p>
        <CityDescription description={city.description} />
      </Container>
      <LocalGroup localGroup={city.local_group} />
      <div className="backgroundColor">
        <Container>
          <SupportingNgos supportingNgos={city.supporting_ngos} />
        </Container>
      </div>
    </>
  );
}
