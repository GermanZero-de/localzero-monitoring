"use client";

import * as React from "react";
import styles from "./styles/ImplementationIndicator.module.scss";
import { TaskStatus } from "@/types/enums";
import {executionLabels} from "@/lib/utils"

type TasksNumber = { complete: number; asPlanned: number; unknown: number; delayed: number; failed: number };

type Props = {
  tasksNumber: TasksNumber;
  startYear: number;
  endYear: number;
};

const taskStatusOrder = [
  TaskStatus.unknown,
  TaskStatus.failed,
  TaskStatus.delayed,
  TaskStatus.asPlanned,
  TaskStatus.complete,
];

const getTotalNumber = (tasksNumber: TasksNumber): number => {
  return Object.values(tasksNumber).reduce((accumulator, currentValue) => accumulator + currentValue, 0);
};

const getTasksHeightsInPercentage = (tasksNumber: TasksNumber, totalNumberOfTasks: number): string[] => {
  const arrowHeightPercentage = 10; // Reserve 10% for the arrow
  const remainingPercentage = 100 - arrowHeightPercentage;

  // Calculate the percentage of each status relative to the remaining percentage
  return taskStatusOrder.map(
    (status) => ((tasksNumber[status] / totalNumberOfTasks) * remainingPercentage).toFixed(2) + "%"
  );
};

// Helper function to calculate the current year position as a percentage along the timeline
const getYearPositionPercentage = (currentYear: number, startYear: number, endYear: number): number => {
  const totalYears = endYear - startYear;
  const yearsPassed = currentYear - startYear;
  return totalYears > 1 ? (yearsPassed / totalYears) * 100 : 90;
};

const ImplementationIndicator: React.FC<Props> = ({ tasksNumber, startYear, endYear }) => {
  const currentYear = new Date().getFullYear(); // Get the current year
  const barWidth = 30;
  const totalNumber = getTotalNumber(tasksNumber);
  const tasksHeights = getTasksHeightsInPercentage(tasksNumber, totalNumber);

  // Calculate the position of the indicator along the timeline
  const currentYearPosition = getYearPositionPercentage(currentYear, startYear, endYear);

  return (
    <div className={styles.wrapper}>
      <div className={styles.timeline}>
        <label>{startYear}</label>
        <label>{endYear}</label>
      </div>

      {/* Position the indicatorContainer along the timeline */}
      <div
        className={styles.indicatorContainer}
        style={{
          width: `${barWidth}px`,
          position: "absolute",
          left: `${currentYearPosition}%`, // Move it along the timeline based on the current year
          transform: "translateX(-50%)", // Center it based on its width
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
                height: tasksHeights[index], // Set height as a percentage
                borderTopLeftRadius: isFirst ? "10px" : "0px",
                borderTopRightRadius: isFirst ? "10px" : "0px",
                width: "100%",
              }}
            ></div>
          );
        })}

        {/* Arrowhead at the bottom */}
        <div className={styles.arrow}></div>
      </div>
    </div>
  );
};

export default ImplementationIndicator;
