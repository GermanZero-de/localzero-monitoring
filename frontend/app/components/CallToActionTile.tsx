import React from "react";
import styles from "./styles/CallToActionTile.module.scss";
import Image from "next/image";
import arrow from "@/public/imgs/arrow-right-down-white.svg";
import iconContact from "@/public/imgs/icon-email.svg";
import iconJoin from "@/public/imgs/icon-join.svg";

interface NavigationTileProps {
  title: string;
  text?: string;
  link: string;
  type: string;
}

const CallToActionTile: React.FC<NavigationTileProps> = ({ title, text, link, type }) => {
  const colorStyle = type === "contact" ? styles.yellow : styles.green;
  return (
    <div className={styles.wrapper}>
    <a
      href={link}
      target="_new"
      className={`${styles.tile} ${colorStyle}`}
    >

      <Image
        className={styles.arrow}
        width={15}
        height={15}
        src={arrow}
        alt="little arrow"
      ></Image>
      <div className={styles.iconWrapper}>
        {type === "contact" ? (
          <Image
            width={40}
            height={30}
            src={iconContact}
            alt="icon"
          />
        ) : (
          <Image
            width={40}
            height={35}
            src={iconJoin}
            alt="icon"
          />
        )}
      </div>
      <div className={styles.content}>
        <h4 className={styles.title}>{title}</h4>
        {text && <h5 className={styles.text}>{text}</h5>}
      </div>

    </a>
    </div>
  );
};

export default CallToActionTile;
