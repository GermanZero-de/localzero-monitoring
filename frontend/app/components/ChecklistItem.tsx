"use client";

import "bootstrap-icons/font/bootstrap-icons.css";
import { AccordionBody, AccordionHeader, AccordionItem } from "react-bootstrap";
import Markdown from "react-markdown";
import styles from "./styles/ChecklistItem.module.scss";

type Props = {
  checklist_item: {
    id: string;
    is_checked: boolean;
    question: string;
    help_text: string;
    rationale: string;
  };
};

const ChecklistItem: React.FC<Props> = ({ checklist_item }) => {
  return (
    <AccordionItem eventKey={checklist_item.id}>
      <AccordionHeader>
        {checklist_item.is_checked ? (
          <i className={`bi-check-circle pe-3 ${styles.checked}`}></i>
        ) : (
          <i className={`bi-circle pe-3 ${styles.unchecked}`}></i>
        )}
        {checklist_item.question}
      </AccordionHeader>
      <AccordionBody>
        {checklist_item.help_text.trim() ? (
          <div>
            <strong>Erklärung:</strong>
            <Markdown>{checklist_item.help_text}</Markdown>
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
    </AccordionItem>
  );
};

export default ChecklistItem;
