import React from "react";
import { Accordion } from "react-bootstrap";
import styles from "./styles/MeasureCard.module.scss";
import LinkMeasureCard from "./LinkMeasureCard";
import SecondaryMeasureCard from "./SecondaryMeasureCard";

interface MeasureCardContentProps {
  text: string;
  tasks: { title: string; parent?: boolean }[];
}

const MeasureCardContent: React.FC<MeasureCardContentProps> = ({ text, tasks }) => {
  return (
    <div>
      {text}
      <Accordion
        defaultActiveKey="0"
        className={styles.accordion}
      >
        {tasks.map((task, i) => {
          if (task.parent) {
            return (
              <SecondaryMeasureCard
                eventKey={i.toString()}
                key={i}
                title={task.title}
              >
                hi{" "}
              </SecondaryMeasureCard>
            );
          } else {
            return (
              <LinkMeasureCard
                eventKey={i.toString()}
                title={task.title}
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
