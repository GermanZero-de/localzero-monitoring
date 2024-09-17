"use client";

import "bootstrap-icons/font/bootstrap-icons.css";
import { AccordionBody, AccordionHeader, AccordionItem } from "react-bootstrap";
import Markdown from "react-markdown";
import styles from "./styles/ChecklistItem.module.scss";
import rehypeRaw from "rehype-raw";
import type { CheckItem } from "@/types";

type Props = {
  checklist_item: CheckItem;
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
        <span style={{fontWeight: checklist_item.is_checked ? "bold" :""}}>{checklist_item.question}</span>
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
              <Markdown rehypePlugins={[rehypeRaw]} className="mdContent">{checklist_item.rationale}</Markdown>
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
