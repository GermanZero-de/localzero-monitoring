import ChecklistItem from "@/app/components/ChecklistItem";
import "bootstrap-icons/font/bootstrap-icons.css";
import { Accordion, Container } from "react-bootstrap";
import Markdown from "react-markdown";
import { getCities } from "@/lib/dataService";

export default async function CapChecklist({ params }: { params: { city: string } }) {

  const city = await getCities(params.city);

  if (!city) {
    return <></>;
  }

  return (
    <Container>
      <div className="pb-3"></div>
      <h2 className="headingWithBar">Klimaaktionsplan {city.name}</h2>
      <Markdown className="pb-3">{city.assessment_action_plan}</Markdown>
      <Accordion
        id="accordionFlushKAP"
        className="accordion-flush pb-3"
      >
        {city.cap_checklist.map((item:any) => (
          <ChecklistItem
            key={item.id}
            checklist_item={item}
          ></ChecklistItem>
        ))}
      </Accordion>
    </Container>
  );
}
