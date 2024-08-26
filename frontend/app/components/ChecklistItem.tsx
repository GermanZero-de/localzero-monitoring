"use client";

import "bootstrap-icons/font/bootstrap-icons.css";
import { AccordionBody, AccordionHeader, AccordionItem } from "react-bootstrap";
import Markdown from "react-markdown";
import styles from "./styles/ChecklistItem.module.scss";
import rehypeRaw from "rehype-raw";
import { ChecklistItem as ChecklistItemType } from "@/types";

type Props = {
  checklist_item: ChecklistItemType;
};

const ChecklistItem: React.FC<Props> = ({ checklist_item }) => {
  return (
    <AccordionItem eventKey={String(checklist_item.id)}>
      <AccordionHeader>
        {checklist_item.is_checked ? (
          <i className={`bi-check-circle pe-3 ${styles.checked}`}></i>
        ) : (
          <i className={`bi-circle pe-3 ${styles.unchecked}`}></i>
        )}
        {checklist_item.question}
      </AccordionHeader>
      {checklist_item.help_text.trim() || checklist_item.rationale.trim() ? (
        <AccordionBody>
          {checklist_item.help_text.trim() ? (
            <div>
              <strong>Erklärung:</strong>
              <Markdown rehypePlugins={[rehypeRaw]}>{checklist_item.help_text}</Markdown>
            </div>
          ) : (
            <></>
          )}
          {checklist_item.rationale.trim() ? (
            <div>
              <strong>Anmerkung / Begründung: </strong>
              <Markdown>{checklist_item.rationale}</Markdown>
            </div>
          ) : (
            <></>
          )}
        </AccordionBody>
      ) : (
        <></>
      )}
    </AccordionItem>
  );
};

export default ChecklistItem;
