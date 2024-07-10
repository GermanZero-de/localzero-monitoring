import React, { useContext } from "react";
import Image from "next/image";
import expandArrowDown from "../../public/images/arrow-expand-down.svg";
import expandArrowUp from "../../public/images/arrow-expand-up.svg";
import { Accordion, AccordionContext, Card, Container, useAccordionButton } from "react-bootstrap";
import styles from "./styles/MeasureCard.module.scss";

interface MeasureCardProps {
  title: string;
  numberOfMeasures: { done: number; inProgress: number; late: number; failed: number; unknown: number };
  children: React.ReactNode;
}

function ContextAwareToggle({ children, eventKey, callback }) {
  const { activeEventKey } = useContext(AccordionContext);

  const decoratedOnClick = useAccordionButton(eventKey, () => callback && callback(eventKey));

  const isCurrentEventKey = activeEventKey === eventKey;

  return (
    <Image
      src={isCurrentEventKey ? expandArrowUp : expandArrowDown}
      alt="Zeige mehr über das Lokalteam"
      onClick={decoratedOnClick}
    />
  );
}

const MeasureCard: React.FC<MeasureCardProps> = ({ title, numberOfMeasures, children }) => {
  const totalNumberOfMeasures = Object.entries(numberOfMeasures).reduce(
    (sum: number, numberOfMeasure: [string, number]) => {
      if (numberOfMeasure[0] !== "unknown") {
        return sum + numberOfMeasure[1];
      }
      return sum;
    },
    0,
  );

  return (
    <Card>
      <Card.Header className={styles.header}>
        <div className={styles.headertitle}>
          <h3>{title}</h3>
          <div>{totalNumberOfMeasures} Maßnahmen im Monitoring</div>
        </div>
        <div className={styles.headersecondrow}>
          <ContextAwareToggle
            eventKey="0"
            callback={(x) => {
              console.log(x);
            }}
          >
            Click me!
          </ContextAwareToggle>
        </div>
      </Card.Header>
      <Accordion.Collapse eventKey="0">
      <div className={styles.content}>{children}</div>
      </Accordion.Collapse>
    </Card>
  );
};

export default MeasureCard;
