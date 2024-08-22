import * as React from "react";
import styles from "./styles/ImplementationIndicator.module.scss";

export enum TaskStatus {
  complete = "complete",
  asPlanned = "asPlanned",
  delayed = "delayed",
  failed = "failed",
  unknown = "unknown",
}

type TasksNumber = { complete: number; asPlanned: number; unknown: number; delayed: number; failed: number };

type Props = {
  tasksNumber: TasksNumber;
};

const taskStatusOrder = [
  TaskStatus.unknown,
  TaskStatus.failed,
  TaskStatus.delayed,
  TaskStatus.asPlanned,
  TaskStatus.complete,
];

const getArrowheadStyle: (taskStatusInPercent: TasksNumber) => string = (taskStatusInPercent) => {
  for (let key in TaskStatus) {
    if (taskStatusInPercent[key as TaskStatus] > 0) {
      return styles[key];
    }
  }
  return styles.complete;
};

const getTotalNumber = (tasksNumber: TasksNumber): number => {
  return Object.values(tasksNumber).reduce((accumulator, currentValue) => accumulator + currentValue, 0);
};

const getTasksHeights = (tasksNumber: TasksNumber, totalNumberOfTasks: number, length: number): number[] => {
  return taskStatusOrder.map((status) => (tasksNumber[status] / totalNumberOfTasks) * length);
};

const getTasksCumulative = (tasksHeights: number[]): number[] => {
  const cumulativeSum = (
    (sum) => (value: number) =>
      (sum += value)
  )(0);
  const tasksCumulative = tasksHeights.map(cumulativeSum);
  tasksCumulative.unshift(0);
  return tasksCumulative;
};

const ImplementationIndicator: React.FC<Props> = ({ tasksNumber: tasksNumber }) => {
  const borderWidth = 1;
  const borderWidthHalf = borderWidth / 2;
  const width = 40;
  const length = 130;
  const totalLength = 150;
  const tasksHeights = getTasksHeights(tasksNumber, getTotalNumber(tasksNumber), length);
  const tasksCumulative = getTasksCumulative(tasksHeights);
  const arrowheadStyle = getArrowheadStyle(tasksNumber);

  return (
    <svg
      viewBox={`0 0 ${width + borderWidth} ${totalLength + borderWidth}`}
      xmlns="http://www.w3.org/2000/svg"
    >
      {taskStatusOrder.map((status, index) => (
        <rect
          key={status}
          className={styles[status]}
          x={borderWidthHalf}
          y={tasksCumulative[index] + borderWidthHalf}
          width={width}
          height={tasksHeights[index]}
        />
      ))}

      <polygon
        className={arrowheadStyle}
        points={`${borderWidthHalf},${length + borderWidthHalf} ${width / 2 + borderWidthHalf},${totalLength + borderWidthHalf} ${width + borderWidthHalf},${length + borderWidthHalf}`}
      />

      <polygon
        points={`${borderWidthHalf},${borderWidthHalf} ${width + borderWidthHalf},${borderWidthHalf} ${width},${length + borderWidthHalf} ${width / 2 + borderWidthHalf},${totalLength + borderWidthHalf} ${borderWidthHalf},${length + borderWidthHalf}`}
        className={styles.implementationIndicator}
      />
    </svg>
  );
};

export default ImplementationIndicator;
