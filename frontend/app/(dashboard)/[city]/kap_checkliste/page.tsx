import ChecklistItem from "@/app/components/ChecklistItem";
import "bootstrap-icons/font/bootstrap-icons.css";
import { Accordion, Container } from "react-bootstrap";
import Markdown from "react-markdown";
import { getCities } from "@/lib/dataService";
import ChecklistIndicator from "@/app/components/ChecklistIndicator";
import type { CheckItem } from "@/types";
import rehypeRaw from "rehype-raw";

export default async function CapChecklist({ params }: { params: { city: string } }) {

  const city = await getCities(params.city);

  if (!city) {
    return <></>;
  }

  return (
    <Container className="w-75">
      <div className="pb-3">
          <ChecklistIndicator
            style={{height:250, marginBottom:30}}
            total={city.cap_checklist.length}
            checked={city.cap_checklist.filter((item: CheckItem) => item.is_checked).length}
            startYear={new Date(city.resolution_date).getFullYear()}
            endYear={city.target_year}
            showLegend
            title="Qualität des KAP"
          />
      </div>
      <h1 className="headingWithBar">Klimaaktionsplan {city.name}</h1>
      <Markdown rehypePlugins={[rehypeRaw]} className="pb-3 mdContent">{city.assessment_action_plan}</Markdown>
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
