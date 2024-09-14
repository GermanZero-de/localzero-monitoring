"use client";

import * as React from "react";
import styles from "./styles/ChecklistIndicator.module.scss";

type Props = {
  total: number;
  checked: number;
  startYear: number;
  endYear: number;
};

const getYearPositionPercentage = (currentYear: number, startYear: number, endYear: number): number => {
  const totalYears = endYear - startYear;
  const yearsPassed = currentYear - startYear;
  return totalYears > 1 ? (yearsPassed / totalYears) * 100 : 90;
};

const ChecklistIndicator: React.FC<Props> = ({ total, checked, startYear, endYear }) => {
  const currentYear = new Date().getFullYear();
  const barWidth = 30;

  const checkedHeight = (checked * 100) / total;
  const currentYearPosition = getYearPositionPercentage(currentYear, startYear, endYear);

  // Ensure a maximum of 10 ticks
  const tickCount = Math.min(total, 10);
  const tickInterval = Math.max(Math.floor(total / tickCount), 1);

  const tickLabels = Array.from({ length: tickCount }, (_, index) => {
    const tickValue = index * tickInterval;
    return tickValue;
  });

  return (
    <div className={styles.wrapper}>
      <div className={styles.timeline}>
        <label>{startYear}</label>
        <label>{endYear}</label>
      </div>
      <div className={styles.ticksContainer}  style={{
          left: `${currentYearPosition+2.5}%`, //
        }}>
          {tickLabels.map((tick, index) => (
            <div key={index} className={styles.tick}>
              {/* Label only for the first, middle, and last tick */}
              {(index === 0 || index === Math.floor(tickCount / 2) || index === tickCount - 1) && (
                <span className={styles.tickLabel}>
                  {index === 0
                    ? total
                    : index === Math.round(tickCount / 2)
                    ? Math.round(total / 2)
                    : 1}
                </span>
              )}
            </div>
          ))}
        </div>
      <div
        className={styles.indicatorContainer}
        style={{
          width: `${barWidth}px`,
          position: "absolute",
          left: `${currentYearPosition}%`, // Move it along the timeline based on the current year
          transform: "translateX(-50%)", // Center it based on its width
        }}
      >
        <div
          style={{
            background: "lightgray",
            height: `${100 - checkedHeight}%`,
            width: "100%",
          }}
        ></div>
        <div
          style={{
            background: "#9bd300",
            height: `${checkedHeight}%`,
            width: "100%",
          }}
        ></div>


        <div className={styles.arrow}></div>



      </div>
    </div>
  );
};

export default ChecklistIndicator;
