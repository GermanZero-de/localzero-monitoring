import ChecklistItem from "@/app/components/ChecklistItem";
import "bootstrap-icons/font/bootstrap-icons.css";
import { Accordion, Container } from "react-bootstrap";
import Markdown from "react-markdown";
import { getCities } from "@/lib/dataService";

export default async function AdministrationChecklist({ params }: { params: { city: string } }) {

  const city = await getCities(params.city);

  if (!city) {
    return <h3 className="pb-3 pt-3">Für die Stadt {params.city} gibt es kein Monitoring</h3>;
  }

  return (
    <Container>
      <div className="pb-3"></div>
      <h2 className="headingWithBar">Nachhaltigkeitsarchitektur in der Verwaltung</h2>
      <Markdown className="pb-3 mdContent">{city.assessment_administration}</Markdown>
      <Accordion
        id="accordionFlushKAP"
        className="accordion-flush pb-3"
      >
        {city.administration_checklist.map((item:any) => (
          <ChecklistItem
            key={item.id}
            checklist_item={item}
          ></ChecklistItem>
        ))}
      </Accordion>
    </Container>
  );
}
