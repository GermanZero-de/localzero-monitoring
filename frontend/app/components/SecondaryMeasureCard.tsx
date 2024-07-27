import React, { useContext } from "react";
import Image from "next/image";
import expandArrowDown from "../../public/images/arrow-expand-down.svg";
import expandArrowUp from "../../public/images/arrow-expand-up.svg";
import { Accordion, AccordionContext, Card, useAccordionButton } from "react-bootstrap";
import styles from "./styles/SecondaryMeasureCard.module.scss";

interface MeasureCardProps {
  eventKey: string;
  title: string;
  children: React.ReactNode;
}

const CardToggle: React.FC<{ eventKey: string }> = ({ eventKey }) => {
  const { activeEventKey } = useContext(AccordionContext);

  const decoratedOnClick = useAccordionButton(eventKey);

  const isCurrentEventKey = activeEventKey === eventKey;

  return (
    <Image
      src={isCurrentEventKey ? expandArrowUp : expandArrowDown}
      alt="Zeige mehr über das Lokalteam"
      onClick={decoratedOnClick}
    />
  );
};

const SecondaryMeasureCard: React.FC<MeasureCardProps> = ({ eventKey, title, children }) => {
  const { activeEventKey } = useContext(AccordionContext);
  const isCurrentEventKey = activeEventKey === eventKey;

  return (
    <Card className={!isCurrentEventKey ? styles.closedcard : ""}>
      <Card.Header className={styles.header}>
        {title}
        <div className={styles.toggle}>
          <CardToggle eventKey={eventKey}></CardToggle>
        </div>
      </Card.Header>
      <Accordion.Collapse eventKey={eventKey}>
        <div className={styles.content}>{children}</div>
      </Accordion.Collapse>
    </Card>
  );
};

export default SecondaryMeasureCard;
