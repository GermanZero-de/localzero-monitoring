"use client";

import * as React from "react";
import styles from "./styles/ChecklistIndicator.module.scss";

type Props = {
  style?: React.CSSProperties;
  total: number;
  checked: number;
  startYear: number;
  endYear: number;
  showLegend?: boolean;
  showNow?: boolean;
  title?: string;
};

const getYearPositionPercentage = (currentYear: number, startYear: number, endYear: number): number => {
  const totalYears = endYear - startYear;
  const yearsPassed = currentYear - startYear;
  let perc = (yearsPassed / totalYears) * 100
  if(perc<0){
    perc=5;
  }else if(perc>100){
    perc=100;
  }
  return totalYears > 1 ? perc : 90;
};

const ChecklistIndicator: React.FC<Props> = ({ total, checked, startYear, endYear, style, title ="", showLegend=false, showNow=false }) => {
  const currentYear = new Date().getFullYear();

  const checkedHeight = (checked * 100) / total;
  const currentYearPosition = getYearPositionPercentage(currentYear, startYear, endYear);

  // Ensure a maximum of 10 ticks
  const tickCount = Math.min(total, 10);
  const tickInterval = Math.max(Math.floor(total / tickCount), 1);

  const tickLabels = Array.from({ length: tickCount }, (_, index) => {
    const tickValue = index * tickInterval;
    return tickValue;
  });

  const legend = showLegend ?  <div className={styles.legend}
  style={{
    overflow: "hidden",
    position: "absolute",
    left: `${(currentYearPosition + 5) > 50 ? 10 : currentYearPosition + 5}%`
  }}>
  <h5 className={styles.title}>{title}</h5>
  <div className={styles.legendItem}>
    <span>Erfüllt {checked} von {total} Kriterien</span>
  </div>
</div> :<></>

  return (
    <div className={styles.wrapper} style={style}>
      {legend}
      <div className={styles.timeline} style={{
        background: `linear-gradient(90deg, #0CA8FF ${currentYearPosition}%, #ccc ${currentYearPosition}%)`
        }}>
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
                    : index === Math.floor(tickCount / 2)
                    ? Math.floor(total / 2)
                    : 1}
                </span>
              )}
            </div>
          ))}
        </div>
      <div
        className={`${styles.indicatorContainer} ${showLegend? "" : styles.small}`}
        style={{
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
