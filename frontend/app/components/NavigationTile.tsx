import React from 'react';
import ArrowRight from "./icons/ArrowRight";
import styles from "./styles/NavigationTile.module.scss";
import Link from "next/link";

interface NavigationTileProps {
  title: string;
  subtitle?: string;
  link: string;
  children: React.ReactNode;
  isBigCard?: boolean;
  className?: string;
}

const NavigationTile: React.FC<NavigationTileProps> = ({ title, subtitle, link = '', isBigCard = false, className, children }) => {
  return (
      <Link href={link} className={`${styles.card} ${isBigCard ? styles.bigcard : ''} ${className}`}>
        <div className={styles.header}>
          <div className={styles.text}>
            {subtitle && <h5 className={styles.subtitle}>{subtitle}</h5>}
            <h3 className={styles.title}>{title}</h3>
          </div>
          <div className={styles.arrow}>
            <ArrowRight color="#ffc80c" />
          </div>
        </div>
        <div className={styles.content}>{children}</div>
      </Link>
  );
};

export default NavigationTile;
