import ChecklistItem from "@/app/components/ChecklistItem";
import "bootstrap-icons/font/bootstrap-icons.css";
import { Accordion, Container } from "react-bootstrap";
import Markdown from "react-markdown";
import { getCities } from "@/lib/dataService";
import ChecklistIndicator from "@/app/components/ChecklistIndicator";
import { CheckItem } from "@/types";
import rehypeRaw from "rehype-raw";
import remarkGfm from 'remark-gfm'

export default async function AdministrationChecklist({ params }: { params: { city: string } }) {

  const city = await getCities(params.city);

  if (!city) {
    return <h3 className="pb-3 pt-3">Für die Stadt {params.city} gibt es kein Monitoring</h3>;
  }

  return (
    <Container className="w-sm-75">
      <div className="pb-3">
          <ChecklistIndicator
            style={{height:250, marginBottom:30}}
            total={city.administration_checklist.length}
            checked={city.administration_checklist.filter((item: CheckItem) => item.is_checked).length}
            startYear={new Date(city.resolution_date).getFullYear()}
            endYear={city.target_year}
            showLegend
            title="Wo steht die Verwaltung?"
          />
      </div>
      <h1 className="headingWithBar">Nachhaltigkeitsarchitektur in der Verwaltung</h1>
      <Markdown rehypePlugins={[rehypeRaw]} remarkPlugins={[remarkGfm]} className="pb-3 mdContent">{city.assessment_administration}</Markdown>
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
