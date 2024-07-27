import React, { useContext } from "react";
import Image from "next/image";
import expandArrowDown from "../../public/images/arrow-expand-down.svg";
import expandArrowUp from "../../public/images/arrow-expand-up.svg";
import { Accordion, AccordionContext, Card, useAccordionButton } from "react-bootstrap";
import styles from "./styles/MeasureCard.module.scss";
import abgeschlossen from "../../public/images/icon-abgeschlossen.svg";
import gescheitert from "../../public/images/icon-gescheitert.svg";
import inArbeit from "../../public/images/icon-in_arbeit.svg";
import unbekannt from "../../public/images/icon-unbekannt.svg";
import verzoegert from "../../public/images/icon-verzoegert_fehlt.svg";

interface MeasureCardProps {
  eventKey: string;
  title: string;
  statusOfSubTasks: { done: number; inProgress: number; late: number; failed: number; unknown: number };
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

const MeasureCard: React.FC<MeasureCardProps> = ({ eventKey, title, statusOfSubTasks, children }) => {
  const totalNumberOfMeasures = Object.entries(statusOfSubTasks).reduce(
    (sum: number, statusOfSubTasks: [string, number]) => {
      if (statusOfSubTasks[0] !== "unknown") {
        return sum + statusOfSubTasks[1];
      }
      return sum;
    },
    0,
  );

  const { activeEventKey } = useContext(AccordionContext);
  const isCurrentEventKey = activeEventKey === eventKey;

  return (
    <Card className={!isCurrentEventKey ? styles.closedcard : ""}>
      <Card.Header className={styles.header}>
        <div className={styles.headertitle}>
          <h3>{title}</h3>
          <div>{totalNumberOfMeasures} Maßnahmen im Monitoring</div>
        </div>
        <div className={styles.headersecondrow}>
          <div className={styles.iconrow}>
            {statusOfSubTasks.done > 0 && (
              <div className={styles.firsticon}>
                <Image
                  src={abgeschlossen}
                  alt="Abgeschlossene Maßnahmen"
                ></Image>
                <h2>{statusOfSubTasks.done}</h2>
              </div>
            )}
            {statusOfSubTasks.inProgress > 0 && (
              <div className={styles.secondicon}>
                <Image
                  src={inArbeit}
                  alt="Maßnahmen in Arbeit"
                ></Image>
                <h2>{statusOfSubTasks.inProgress}</h2>
              </div>
            )}
            {statusOfSubTasks.late > 0 && (
              <div className={styles.thirdicon}>
                <Image
                  src={verzoegert}
                  alt="Verzögerte Maßnahmen"
                ></Image>
                <h2>{statusOfSubTasks.late}</h2>
              </div>
            )}
            {statusOfSubTasks.failed > 0 && (
              <div className={styles.fourthicon}>
                <Image
                  src={gescheitert}
                  alt="Gescheiterte Maßnahmen"
                ></Image>
                <h2>{statusOfSubTasks.failed}</h2>
              </div>
            )}
            {statusOfSubTasks.unknown > 0 && (
              <div className={styles.fifthicon}>
                <Image
                  src={unbekannt}
                  alt="Unbekannte Maßnahmen"
                ></Image>
                <h2>{statusOfSubTasks.unknown}</h2>
              </div>
            )}
          </div>
          <div className={styles.toggle}>
            <CardToggle eventKey={eventKey}></CardToggle>
          </div>
        </div>
      </Card.Header>
      <Accordion.Collapse eventKey={eventKey}>
        <div className={styles.content}>{children}</div>
      </Accordion.Collapse>
    </Card>
  );
};

export default MeasureCard;
