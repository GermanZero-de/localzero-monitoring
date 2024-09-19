"use client";

import * as React from "react";
import styles from "./styles/ImplementationIndicator.module.scss";
import { TaskStatus } from "@/types/enums";
import { executionLabels } from "@/lib/utils"
import { StatusCount } from "@/types";


type Props = {
  style?: React.CSSProperties;
  tasksNumber: StatusCount;
  startYear: number;
  endYear: number;
  showLegend?: boolean;
  showNow?: boolean;
};

const taskStatusOrder = [
  TaskStatus.unknown,
  TaskStatus.failed,
  TaskStatus.delayed,
  TaskStatus.asPlanned,
  TaskStatus.complete,
];

const getTotalNumber = (tasksNumber: StatusCount): number => {
  return Object.values(tasksNumber).reduce((accumulator, currentValue) => accumulator + currentValue, 0);
};

const getTasksHeightsInPercentage = (tasksNumber: StatusCount, totalNumberOfTasks: number): string[] => {
  const arrowHeightPercentage = 10; // Reserve 10% for the arrow
  const remainingPercentage = 100 - arrowHeightPercentage;

  return taskStatusOrder.map(
    (status) => ((tasksNumber[status] / totalNumberOfTasks) * remainingPercentage).toFixed(2) + "%"
  );
};

const getYearPositionPercentage = (currentYear: number, startYear: number, endYear: number): number => {
  const totalYears = endYear - startYear;
  const yearsPassed = currentYear - startYear;
  const perc = ((yearsPassed / totalYears) * 100) < 0 ? 0 : (yearsPassed / totalYears)* 100;
  return totalYears > 1 ? perc : 90;
};

const getFirstNonZeroTaskColor = (tasksNumber: StatusCount) => {
  const colorMap: Record<TaskStatus, string> = {
    [TaskStatus.unknown]: styles.unknown,
    [TaskStatus.failed]: styles.failed,
    [TaskStatus.delayed]: styles.delayed,
    [TaskStatus.asPlanned]: styles.asPlanned,
    [TaskStatus.complete]: styles.complete,
  };

  for (let i = taskStatusOrder.length - 1; i >= 0; i--) {
    const status = taskStatusOrder[i];
    if (tasksNumber[status] > 0) {
      return colorMap[status];
    }
  }
  return styles.unknown;
};


const ImplementationIndicator: React.FC<Props> = ({ tasksNumber, startYear, endYear, style, showLegend=false, showNow=false }) => {
  const currentYear = new Date().getFullYear();
  const totalNumber = getTotalNumber(tasksNumber);
  const tasksHeights = getTasksHeightsInPercentage(tasksNumber, totalNumber);

  const currentYearPosition = getYearPositionPercentage(currentYear, startYear, endYear);
  const arrowColorClass = getFirstNonZeroTaskColor(tasksNumber);

  const now = showNow ? <h5 style={{transform: "translateX(-50%)",left: `${currentYearPosition}%`,bottom:-30, position:"absolute"}}>{new Date().toLocaleDateString()}</h5> : <></>
  const legend = showLegend ?  <div className={styles.legend}
  style={{
    overflow: "hidden",
    position: "absolute",
    left: `${(currentYearPosition + 5) > 50 ? 10 : currentYearPosition + 5}%`
  }}>
  <h5 className={styles.title}>Stand der beobachteten Maßnahmen</h5>
  <div className={styles.legendItem}>
    <div className={`${styles.legendColor} ${styles.unknown}`}></div>
    <span>{executionLabels.unknown}</span>
  </div>
  <div className={`${styles.legendItem}`}>
    <div className={`${styles.legendColor} ${styles.failed}`}></div>
    <span>{executionLabels.failed}</span>
  </div>
  <div className={`${styles.legendItem}`}>
    <div className={`${styles.legendColor} ${styles.delayed}`}></div>
    <span>{executionLabels.delayed}</span>
  </div>
  <div className={`${styles.legendItem}`}>
    <div className={`${styles.legendColor} ${styles.asPlanned}`}></div>
    <span>{executionLabels.asPlanned}</span>
  </div>
  <div className={styles.legendItem}>
    <div className={`${styles.legendColor} ${styles.complete}`}></div>
    <span>{executionLabels.complete}</span>
  </div>
</div> :<></>

  return (
    <div className={styles.wrapper} style={style}>
      <div className={`${styles.timeline} ${showLegend? "" : styles.small}`} style={{
        background: `linear-gradient(90deg, #0CA8FF ${currentYearPosition}%, #ccc ${currentYearPosition}%)`
      }}>
        <label>{startYear}</label>
        <label>{endYear}</label>
      </div>
      {now}
      <div style={{ display: 'flex' }}>

        <div
          className={`${styles.indicatorContainer} ${showLegend? "" : styles.small}`}
          style={{
            position: "absolute",
            left: `${currentYearPosition}%`,
            transform: "translateX(-50%)",
          }}
        >
          {taskStatusOrder.map((status, index) => {
            const isFirst = index === 0;
            return (
              <div
                key={status}
                className={styles[status]}
                title={`${tasksNumber[status]} Maßnahmen ${executionLabels[status]}`}
                style={{
                  height: tasksHeights[index],
                  borderTopLeftRadius: isFirst ? "10px" : "0px",
                  borderTopRightRadius: isFirst ? "10px" : "0px",
                  width: "100%",
                }}
              ></div>
            );
          })}
          <div className={`${styles.arrow} ${arrowColorClass}`}></div>
        </div>
      </div>
      {legend}
    </div>
  );
};

export default ImplementationIndicator;
