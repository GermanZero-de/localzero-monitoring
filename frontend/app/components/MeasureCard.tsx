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
        onClick={(e)=>{
          const newUrl = new URL(window.location.href);
          newUrl.searchParams.set('active', eventKey);
          newUrl.hash=`#${eventKey}`;
          window.history.pushState({}, '', newUrl.toString());
          onClick(e)
        }}
      >
        <div className={styles.headertitle}>
          <h4 id={eventKey} style={{scrollMarginTop:200}}>{title}</h4>
          <div>{totalNumberOfMeasures} Maßnahmen im Monitoring</div>
        </div>
        <div className={styles.headersecondrow}>
          <div className={styles.iconrow}>

              <div className={styles.firsticon}>
                <ExecutionStatusIcon disabled={statusOfSubTasks.complete===0} taskStatus={ExecutionStatus.COMPLETE}></ExecutionStatusIcon>
                {statusOfSubTasks.complete > 0 && ( <h4>{statusOfSubTasks.complete}</h4>  )}
              </div>


              <div className={styles.secondicon}>
                <ExecutionStatusIcon disabled={statusOfSubTasks.asPlanned===0} taskStatus={ExecutionStatus.AS_PLANNED}></ExecutionStatusIcon>
                {statusOfSubTasks.asPlanned > 0 && (<h4>{statusOfSubTasks.asPlanned}</h4> )}
              </div>


              <div className={styles.thirdicon}>
                <ExecutionStatusIcon disabled={statusOfSubTasks.delayed===0} taskStatus={ExecutionStatus.DELAYED}></ExecutionStatusIcon>
                {statusOfSubTasks.delayed > 0 && (    <h4>{statusOfSubTasks.delayed}</h4>   )}
              </div>


              <div className={styles.fourthicon}>
                <ExecutionStatusIcon disabled={statusOfSubTasks.failed===0}  taskStatus={ExecutionStatus.FAILED}></ExecutionStatusIcon>
                {statusOfSubTasks.failed > 0 && ( <h4>{statusOfSubTasks.failed}</h4>    )}
              </div>


              <div className={styles.fifthicon}>
                <ExecutionStatusIcon  disabled={statusOfSubTasks.unknown===0} taskStatus={ExecutionStatus.UNKNOWN}></ExecutionStatusIcon>
                {statusOfSubTasks.unknown > 0 && (  <h4>{statusOfSubTasks.unknown}</h4>  )}
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
