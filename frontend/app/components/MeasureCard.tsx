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
          <h3>{title}</h3>
          <div>{totalNumberOfMeasures} Maßnahmen im Monitoring</div>
        </div>
        <div className={styles.headersecondrow}>
          <div className={styles.iconrow}>
            {statusOfSubTasks.done > 0 && (
              <div className={styles.firsticon}>
                <ExecutionStatusIcon taskStatus={ExecutionStatus.COMPLETE}></ExecutionStatusIcon>
                <h2>{statusOfSubTasks.done}</h2>
              </div>
            )}
            {statusOfSubTasks.inProgress > 0 && (
              <div className={styles.secondicon}>
                <ExecutionStatusIcon taskStatus={ExecutionStatus.AS_PLANNED}></ExecutionStatusIcon>
                <h2>{statusOfSubTasks.inProgress}</h2>
              </div>
            )}
            {statusOfSubTasks.late > 0 && (
              <div className={styles.thirdicon}>
                <ExecutionStatusIcon taskStatus={ExecutionStatus.DELAYED}></ExecutionStatusIcon>
                <h2>{statusOfSubTasks.late}</h2>
              </div>
            )}
            {statusOfSubTasks.failed > 0 && (
              <div className={styles.fourthicon}>
                <ExecutionStatusIcon taskStatus={ExecutionStatus.FAILED}></ExecutionStatusIcon>
                <h2>{statusOfSubTasks.failed}</h2>
              </div>
            )}
            {statusOfSubTasks.unknown > 0 && (
              <div className={styles.fifthicon}>
                <ExecutionStatusIcon taskStatus={ExecutionStatus.UNKNOWN}></ExecutionStatusIcon>
                <h2>{statusOfSubTasks.unknown}</h2>
              </div>
            )}
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
