"use client";

import { useGetCity } from "@/app/CityService";
import Image from "next/image";

import MeasureCard from "@/app/components/MeasureCard";
import { usePathname } from "next/navigation";
import { Accordion, Card, Container } from "react-bootstrap";
import styles from "./page.module.scss";
import abgeschlossen from "../../../public/images/icon-abgeschlossen.svg";
import gescheitert from "../../../public/images/icon-gescheitert.svg";
import inArbeit from "../../../public/images/icon-in_arbeit.svg";
import unbekannt from "../../../public/images/icon-unbekannt.svg";
import verzoegert from "../../../public/images/icon-verzoegert_fehlt.svg";

export default function CityMeasures() {
  const pathname = usePathname();
  const slug = pathname.split("/").at(-2);
  const { city, hasError } = useGetCity(slug);

  if (!city || hasError) {
    return <></>;
  }

  const numberOfElectrictyMeasures = { done: 2, inProgress: 2, late: 1, failed: 1, unknown: 5 };
  const numberOfEBuildingMeasures = { done: 0, inProgress: 2, late: 0, failed: 7, unknown: 5 };
console.log(city)
  return (
    <Container className={styles.container}>
      <h2 className="headingWithBar">Maßnahmen in {city.name}</h2>
      <Accordion
        defaultActiveKey="0"
        className={styles.accordion}
      >
        <MeasureCard
          eventKey="0"
          title="Strom"
          numberOfMeasures={numberOfElectrictyMeasures}
        >
          <Card.Body>Hello! I am the body</Card.Body>
        </MeasureCard>
        <MeasureCard
          eventKey="1"
          title="Wärme und Gebäude"
          numberOfMeasures={numberOfEBuildingMeasures}
        >
          <Card.Body>Hello! I am the body</Card.Body>
        </MeasureCard>
      </Accordion>
      <div className={styles.legende}>
        <div>
          <Image
            src={abgeschlossen}
            alt="Abgeschlossene Maßnahmen"
          ></Image>abgeschlossen
        </div>
        <div>
          <Image
                  src={inArbeit}
                  alt="Maßnahmen in Arbeit"
          ></Image>in Arbeit
        </div>
        <div>
          <Image
                  src={verzoegert}
                  alt="Verzögerte Maßnahmen"
          ></Image>verzögert
        </div>
        <div>
          <Image
                  src={gescheitert}
                  alt="Gescheiterte Maßnahmen"
          ></Image>gescheitert
        </div>
        <div>
          <Image
                  src={unbekannt}
                  alt="Unbekannte Maßnahmen"
          ></Image>unbekannt
        </div>
      </div>
    </Container>
  );
}
