import * as React from "react";
import styles from "./styles/ImplementationIndicator.module.scss";

export enum TaskStatus {
  complete = "complete",
  asPlanned = "asPlanned",
  delayed = "delayed",
  failed = "failed",
  unknown = "unknown",
}

type tasksNumberType = { complete: number; asPlanned: number; unknown: number; delayed: number; failed: number };

type Props = {
  tasksNumber: tasksNumberType;
};

const taskStatusOrder = [TaskStatus.unknown, TaskStatus.failed, TaskStatus.delayed, TaskStatus.asPlanned, TaskStatus.complete];

const getArrowheadStyle: (taskStatusInPercent: tasksNumberType) => string = (taskStatusInPercent) => {
  for (let key in TaskStatus) {
    if (taskStatusInPercent[key as TaskStatus] > 0) {
      return styles[key];
    }
  }
  return styles.complete;
};

const getTotalNumber = (tasksNumber: tasksNumberType): number => {
  return Object.values(tasksNumber).reduce((accumulator, currentValue) => accumulator + currentValue, 0);
};

const getTasksHeights = (
  tasksNumber: tasksNumberType,
  totalNumberOfTasks: number,
  length: number,
): number[] => {
  return taskStatusOrder.map((status) => tasksNumber[status] / totalNumberOfTasks * length);
};

const getTasksCumulative = (tasksHeights: number[]): number[] => {
  const cumulativeSum = (sum => (value: number) => sum += value)(0);
  const tasksCumulative = tasksHeights.map(cumulativeSum);
  tasksCumulative.unshift(0);
  return tasksCumulative;
};

const ImplementationIndicator: React.FC<Props> = ({tasksNumber: tasksNumber}) => {
  const borderWidth = 1;
  const borderWidthHalf = borderWidth / 2;
  const width = 40;
  const length = 130;
  const totalLength = 150;
  const tasksHeights = getTasksHeights(tasksNumber, getTotalNumber(tasksNumber), length);
  const tasksCumulative = getTasksCumulative(tasksHeights);
  const tasksStyle =  taskStatusOrder.map((status) => styles[status])
  const arrowheadStyle = getArrowheadStyle(tasksNumber);

  return (
    <svg
      width={width + 2 * borderWidth}
      height={totalLength + 2 * borderWidth}
      xmlns="http://www.w3.org/2000/svg"
    >
      {taskStatusOrder.map((status, index) => (
            <rect
              key={status}
              className={tasksStyle[index]}
              x={borderWidthHalf}
              y={tasksCumulative[index] + borderWidthHalf}
              width={width}
              height={tasksHeights[index]}
            />
      ))}

      <polygon
        className={arrowheadStyle}
        points={`${borderWidthHalf},${length + borderWidthHalf} ${width/2 + borderWidthHalf},${totalLength+ borderWidthHalf} ${width + borderWidthHalf},${length+ borderWidthHalf}`}
      />

      <polygon
        points={`${borderWidthHalf},${borderWidthHalf} ${width + borderWidthHalf},${borderWidthHalf} ${width},${length + borderWidthHalf} ${width/2 + borderWidthHalf},${totalLength+borderWidthHalf} ${borderWidthHalf},${length+borderWidthHalf}`}
        className={styles.implementationIndicator}
      />
    </svg>
  );
};

export default ImplementationIndicator;
