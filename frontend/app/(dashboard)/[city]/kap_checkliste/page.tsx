import ChecklistItem from "@/app/components/ChecklistItem";
import "bootstrap-icons/font/bootstrap-icons.css";
import { Accordion, Container } from "react-bootstrap";
import Markdown from "react-markdown";
import { getCities } from "@/lib/dataService";
import ChecklistIndicator from "@/app/components/ChecklistIndicator";
import type { CheckItem } from "@/types";
import rehypeRaw from "rehype-raw";
import remarkGfm from 'remark-gfm'

// @next-codemod-ignore Cache Components adoption: this segment temporarily allows blocking.
// Remove this opt-out after verifying the segment passes validation without it.
// See: https://nextjs.org/docs/app/guides/migrating-to-cache-components
export const instant = false;

export default async function CapChecklist(props: { params: Promise<{ city: string }> }) {
  const params = await props.params;

  const city = await getCities(params.city);

  if (!city) {
    return <></>;
  }

  return (
    <Container className="w-sm-75">
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
      <div className="pb-3 mdContent">
        <Markdown rehypePlugins={[rehypeRaw]} remarkPlugins={[remarkGfm]}>{city.assessment_action_plan}</Markdown>
      </div>
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
