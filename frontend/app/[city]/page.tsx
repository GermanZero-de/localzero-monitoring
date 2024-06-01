"use client";

import Image from "next/image";
import { usePathname } from "next/navigation";
import { useState } from "react";
import { Container } from "react-bootstrap";
import Markdown from "react-markdown";
import arrow from "../../public/images/arrow-right-down.svg";
import { useGetCity } from "../CityService";
import LocalGroup from "../components/LocalGroup";

const CityDescription = ({ description }) => {
  if (!description) {
    return <></>;
  }
  return (
    <>
      <h2 className="headingWithBar">Klimaschutz in München</h2>
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
      <h2 className="headingWithBar">Mit Unterstützung von</h2>
      <Markdown className="block-text pb-3">{supportingNgos}</Markdown>
    </>
  );
};

export default function CityDashboard() {
  const [isLocalGroupExpanded, setIsLocalGroupExpanded] = useState(false);

  const pathname = usePathname();
  const slug = pathname.split("/").at(-1);

  const { city, hasError } = useGetCity(slug);

  if (hasError) {
    return <h3 className="pb-3 pt-3">Für die Stadt {slug} gibt es kein Monitoring</h3>;
  }

  if (!city) {
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
      <LocalGroup
        localGroup={city.local_group}
        isExpanded={isLocalGroupExpanded}
        setIsExpanded={setIsLocalGroupExpanded}
      />
      <div className={isLocalGroupExpanded ? "dontDisplay" : "backgroundColor"}>
        <Container>
          <SupportingNgos supportingNgos={city.supporting_ngos} />
        </Container>
      </div>
    </>
  );
}
