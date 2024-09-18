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
  activeKey: string;
}

const MeasureCardContent: React.FC<MeasureCardContentProps> = ({ text, tasks, slugs, eventKey, activeKey="" }) => {

  return (
    <div >
      {text} <a href={"./massnahmen/"+slugs}>Mehr lesen...</a>
      <Accordion className={styles.contentaccordion} defaultActiveKey={activeKey}>
        {tasks.map((task, i) => {
          if (task.numchild && task.children.length > 0) {
            return (
              <SecondaryMeasureCard
                eventKey={task.slugs}
                key={i}
                title={task.title}
                source={task.source}
              >
                <MeasureCardContent
                  activeKey={activeKey}
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
