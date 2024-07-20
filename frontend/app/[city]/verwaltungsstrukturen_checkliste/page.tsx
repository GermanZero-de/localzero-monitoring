"use client";

import { useGetCity } from "@/app/CityService";
import ChecklistItem from "@/app/components/ChecklistItem";
import "bootstrap-icons/font/bootstrap-icons.css";
import { usePathname } from "next/navigation";
import { Accordion, Container } from "react-bootstrap";
import Markdown from "react-markdown";

export default function AdministrationChecklist() {
  const pathname = usePathname();
  const slug = pathname.split("/").at(-2);

  const { city, hasError } = useGetCity(slug);

  if (!city || hasError) {
    return <></>;
  }

  return (
    <Container>
      <div className="pb-3"></div>
      <h2 className="headingWithBar">Nachhaltigkeitsarchitektur in der Verwaltung</h2>
      <Markdown className="pb-3">{city.assessment_administration}</Markdown>
      <Accordion
        id="accordionFlushKAP"
        className="accordion-flush pb-3"
      >
        {city.administration_checklist.map((item) => (
          <ChecklistItem
            key={item.id}
            checklist_item={item}
          ></ChecklistItem>
        ))}
      </Accordion>
    </Container>
  );
}
