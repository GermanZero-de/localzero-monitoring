"use client";
import * as React from "react";
import styles from "./styles/Tile.module.scss";
import Image from "next/image";
import arrow from "../../public/images/arrow-right.svg";

const icons = {
  facebook:
    '<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="28" height="28" viewBox="0 0 28 28"><defs><path id="vsxwc570mb" d="M0 0L11.118 0 11.118 21 0 21z"/></defs><g fill="#011633" fill-rule="evenodd"><g fill="#011633"><g fill="#011633"><g transform="translate(-905 -79) translate(894 68.023) translate(11.5 11.5)"><g transform="translate(7.941 3)"><path fill="#011633" d="M7.216 21v-9.58h3.278l.491-3.732H7.216V5.304c0-1.08.306-1.817 1.886-1.817l2.016-.001V.147C10.769.102 9.573 0 8.18 0 5.275 0 3.286 1.74 3.286 4.935v2.753H0v3.733h3.286V21h3.93z" mask="url(#nlkbp0pfxc)"/></g></g></g></g></g></svg>',
};

type Props = {
  name: string;
  logo: string;
};

const Tile: React.FC<Props> = ({ name, logo }) => {
  let image = null;

  if (!!logo) {
    image = (
      <div className={styles.image}>
        <Image
          width={100}
          height={100}
          src={"http://127.0.0.1:8000" + logo}
          alt={"Logo von " + name}
        />
      </div>
    );
  }

  return (
    <div className={styles.wrapper}>
      <div className={styles.heading}>
        {name}
        <Image
          width={30}
          height={30}
          src={arrow}
          alt="arrow right"
        ></Image>
      </div>
      {image}
    </div>
  );
};

export default Tile;
