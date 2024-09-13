"use client"

import React, { useContext } from "react";
import Image from "next/image";
import expandArrowDown from "@/public/imgs/arrow-expand-down.svg";
import expandArrowUp from "@/public/imgs/arrow-expand-up.svg";
import { Accordion, AccordionContext, Card, useAccordionButton } from "react-bootstrap";
import styles from "./styles/SecondaryMeasureCard.module.scss";
import { TaskSource } from "@/types/enums";


interface MeasureCardProps {
  eventKey: string;
  title: string;
  children: React.ReactNode;
  source: TaskSource
}

const SecondaryMeasureCard: React.FC<MeasureCardProps> = ({ eventKey, title, children, source }) => {
  const { activeEventKey } = useContext(AccordionContext);
  const onClick = useAccordionButton(eventKey);

  const isCurrentEventKey = activeEventKey === eventKey;
  const suggested =   source === TaskSource.suggested ? <div className={styles.suggested}></div> : <></>
  return (
    <Card className={!isCurrentEventKey ? styles.closedcard : ""}>
      {suggested}
      <Card.Header
        className={`${styles.header} ${styles.noicon}`}
        onClick={onClick}
      >
        {title}
        <div className={styles.toggle}>
          <Image
            src={isCurrentEventKey ? expandArrowUp : expandArrowDown}
            alt="Zeige mehr über die Massnahme"
          />
        </div>
      </Card.Header>
      <Accordion.Collapse eventKey={eventKey}>
        <Card.Body className={styles.content}>{children}</Card.Body>
      </Accordion.Collapse>
    </Card>
  );
};

export default SecondaryMeasureCard;
