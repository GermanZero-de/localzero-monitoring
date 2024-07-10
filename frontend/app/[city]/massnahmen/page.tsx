"use client";

import { useGetCity } from "@/app/CityService";
import MeasureCard from "@/app/components/MeasureCard";
import { usePathname } from "next/navigation";
import { Accordion, Card, Container } from "react-bootstrap";

export default function CityMeasures() {
  const pathname = usePathname();
  const slug = pathname.split("/").at(-2);
  const { city, hasError } = useGetCity(slug);

  if (!city || hasError) {
    return <></>;
  }

  const numberOfElectrictyMeasures = { done: 2, inProgress: 2, late: 1, failed: 1, unknown: 5 };

  return (
    <Container className="mt-3">
      <h2 className="headingWithBar">Maßnahmen in {city.name}</h2>
      <Accordion defaultActiveKey="0">
        <MeasureCard
          title="Strom"
          numberOfMeasures={numberOfElectrictyMeasures}
        >        <Card.Body>Hello! I am the body</Card.Body>
        </MeasureCard>
      </Accordion>
    </Container>
  );
}
