import React from "react";
import { Accordion } from "react-bootstrap";
import styles from "./styles/MeasureCard.module.scss";
import LinkMeasureCard from "./LinkMeasureCard";
import SecondaryMeasureCard from "./SecondaryMeasureCard";
import { Task } from "@/types";

interface MeasureCardContentProps {
  text: string;
  tasks: Task[];
  eventKey: string;
}

const MeasureCardContent: React.FC<MeasureCardContentProps> = ({ text, tasks, eventKey }) => {
  return (
    <div>
      {text}
      <Accordion className={styles.contentaccordion}>
        {tasks.map((task, i) => {
          if (task.numchild && task.children.length > 0) {
            return (
              <SecondaryMeasureCard
                eventKey={`p${eventKey}c${i}`}
                key={i}
                title={task.title}
              >
                <MeasureCardContent
                  text={task.description}
                  tasks={task.children}
                  eventKey={`p${eventKey}c${i}`}
                ></MeasureCardContent>
              </SecondaryMeasureCard>
            );
          } else {
            return (
              <LinkMeasureCard
                slugs={task.slugs}
                title={task.title}
                taskStatus={task.execution_status}
                key={i}
              ></LinkMeasureCard>
            );
          }
        })}
      </Accordion>
    </div>
  );
};

export default MeasureCardContent;
