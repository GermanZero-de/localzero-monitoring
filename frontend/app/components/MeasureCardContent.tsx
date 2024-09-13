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
  slugs: string;
}

const MeasureCardContent: React.FC<MeasureCardContentProps> = ({ text, tasks, slugs, eventKey }) => {
  return (
    <div >
      {text} <a href={"./massnahmen/"+slugs}>Mehr lesen...</a>
      <Accordion className={styles.contentaccordion}>
        {tasks.map((task, i) => {
          if (task.numchild && task.children.length > 0) {
            return (
              <SecondaryMeasureCard
                eventKey={`p${eventKey}c${i}`}
                key={i}
                title={task.title}
                source={task.source}
              >
                <MeasureCardContent
                  slugs={task.slugs}
                  text={task.teaser}
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
                source={task.source}
              ></LinkMeasureCard>
            );
          }
        })}
      </Accordion>
    </div>
  );
};

export default MeasureCardContent;
