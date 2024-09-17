import React from "react";
import ArrowRight from "./icons/ArrowRight";
import styles from "./styles/NavigationTile.module.scss";

interface NavigationTileProps {
  title: string;
  subtitle?: string;
  children: React.ReactNode;
  isBigCard?: boolean;
  className?: string;
}

const NavigationTile: React.FC<NavigationTileProps> = ({
  title,
  subtitle,
  isBigCard = false,
  className,
  children,
}) => {
  return (
    <div
      className={`${styles.card} ${isBigCard ? styles.bigcard : ""} ${className}`}
    >
      <div className={styles.header}>
        <div className={styles.text}>
          {subtitle && <h5 className={styles.subtitle}>{subtitle}</h5>}
          <h4 className={styles.title}>{title}</h4>
        </div>
        <div className={styles.arrow}>
          <ArrowRight color="#ffc80c" />
        </div>
      </div>
      <div className={styles.content}>{children}</div>
    </div>
  );
};

export default NavigationTile;
