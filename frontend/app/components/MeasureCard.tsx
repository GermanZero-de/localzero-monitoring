"use client";

import React, { useContext } from "react";
import Image from "next/image";
import expandArrowDown from "@/public/imgs/arrow-expand-down.svg";
import expandArrowUp from "@/public/imgs/arrow-expand-up.svg";
import { Accordion, AccordionContext, Card, useAccordionButton } from "react-bootstrap";
import styles from "./styles/MeasureCard.module.scss";
import ExecutionStatusIcon from "./ExecutionStatusIcon";
import { ExecutionStatus } from "@/types/enums";
import type { StatusCount } from "@/types";

interface MeasureCardProps {
  eventKey: string;
  title: string;
  statusOfSubTasks: StatusCount;
  children: React.ReactNode;
}

const CardToggle: React.FC<{ isCurrentEventKey: boolean }> = ({ isCurrentEventKey }) => {
  return (
    <Image
      src={isCurrentEventKey ? expandArrowUp : expandArrowDown}
      alt="Zeige mehr über das Lokalteam"
    />
  );
};

const MeasureCard: React.FC<MeasureCardProps> = ({ eventKey, title, statusOfSubTasks, children }) => {
  const totalNumberOfMeasures = Object.entries(statusOfSubTasks).reduce(
    (sum: number, statusOfSubTasks: [string, number]) => {
      return sum + statusOfSubTasks[1];
    },
    0,
  );

  const { activeEventKey } = useContext(AccordionContext);
  const isCurrentEventKey = activeEventKey === eventKey;
  const onClick = useAccordionButton(eventKey);
  return (
    <Card className={!isCurrentEventKey ? styles.closedcard : ""}>
      <Card.Header
        className={styles.header}
        onClick={onClick}
      >
        <div className={styles.headertitle}>
          <h3 id={eventKey}>{title}</h3>
          <div>{totalNumberOfMeasures} Maßnahmen im Monitoring</div>
        </div>
        <div className={styles.headersecondrow}>
          <div className={styles.iconrow}>

              <div className={styles.firsticon}>
                <ExecutionStatusIcon disabled={statusOfSubTasks.done===0} taskStatus={ExecutionStatus.COMPLETE}></ExecutionStatusIcon>
                {statusOfSubTasks.done > 0 && ( <h2>{statusOfSubTasks.done}</h2>  )}
              </div>


              <div className={styles.secondicon}>
                <ExecutionStatusIcon disabled={statusOfSubTasks.inProgress===0} taskStatus={ExecutionStatus.AS_PLANNED}></ExecutionStatusIcon>
                {statusOfSubTasks.inProgress > 0 && (<h2>{statusOfSubTasks.inProgress}</h2> )}
              </div>


              <div className={styles.thirdicon}>
                <ExecutionStatusIcon disabled={statusOfSubTasks.late===0} taskStatus={ExecutionStatus.DELAYED}></ExecutionStatusIcon>
                {statusOfSubTasks.late > 0 && (    <h2>{statusOfSubTasks.late}</h2>   )}
              </div>


              <div className={styles.fourthicon}>
                <ExecutionStatusIcon disabled={statusOfSubTasks.failed===0}  taskStatus={ExecutionStatus.FAILED}></ExecutionStatusIcon>
                {statusOfSubTasks.failed > 0 && ( <h2>{statusOfSubTasks.failed}</h2>    )}
              </div>


              <div className={styles.fifthicon}>
                <ExecutionStatusIcon  disabled={statusOfSubTasks.unknown===0} taskStatus={ExecutionStatus.UNKNOWN}></ExecutionStatusIcon>
                {statusOfSubTasks.unknown > 0 && (  <h2>{statusOfSubTasks.unknown}</h2>  )}
              </div>

          </div>
          <div className={styles.toggle}>
            <CardToggle isCurrentEventKey={isCurrentEventKey}></CardToggle>
          </div>
        </div>
      </Card.Header>
      <Accordion.Collapse eventKey={eventKey}>
        <Card.Body className={styles.content}>{children}</Card.Body>
      </Accordion.Collapse>
    </Card>
  );
};

export default MeasureCard;
