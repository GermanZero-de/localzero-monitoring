"use client";

import Image from "next/image";
import { usePathname } from "next/navigation";
import { useState } from "react";
import { Container } from "react-bootstrap";
import Markdown from "react-markdown";
import arrow from "../../public/images/arrow-right-down.svg";
import greenCity from "../../public/background-green-city.png"
import { useGetCity } from "../CityService";
import LocalGroup from "../components/LocalGroup";
import NavigationTile from "@/app/components/NavigationTile";
import styles from "./page.module.scss"

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
        <div className="p-3">
          <div className={styles.tileRowContainer}>
            <NavigationTile className={styles.tile} isBigCard title={"Alles klar in " + city.name + "?"} subtitle="Einleitung">
              <Image style={{width: "100%", height: "100%"}} src={greenCity} alt=""
              />
            </NavigationTile>
            <NavigationTile className={styles.tile} isBigCard title="Stand der Maßnahmen" subtitle="Umsetzung Klimaaktionsplan">"Bild"</NavigationTile>
          </div>
          <div className={styles.tileRowContainer}>
            <NavigationTile className={styles.tile} title="Klimaaktionsplan (KAP)" link={ city.slug + '/kap_checkliste'}>"Bild"</NavigationTile>
            <NavigationTile className={styles.tile} title="Wärmeplanung">"Bild"</NavigationTile>
            <NavigationTile className={styles.tile} title="Wo steht die Verwaltung?" link={ city.slug + '/verwaltungsstrukturen_checkliste'}>"Bild"</NavigationTile>
          </div>
        </div>
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

