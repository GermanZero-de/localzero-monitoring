"use client";

import Image from "next/image";
import { Container } from "react-bootstrap";
import Markdown from "react-markdown";
import expandArrowDown from "@/public/imgs/arrow-expand-down.svg";
import expandArrowUp from "@/public/imgs/arrow-expand-up.svg";
import styles from "./styles/LocalGroup.module.scss";

type Props = {
  localGroup: LocalGroupType;
  isExpanded: boolean;
};

type LocalGroupType = {
  name: string;
  teaser: string;
  featured_image: string;
  description: string;
};

export default function LocalGroup({ localGroup, isExpanded }: Props) {
  if (!localGroup) {
    return <></>;
  }

  let image;

  if(localGroup.featured_image){
    image =  <img
    className="pb-3"
    src={"./" + localGroup.featured_image}
    alt={"Lokalgruppe " + localGroup.name}
  ></img>
  }

  return (
    <div className={isExpanded ? styles.fixed : styles.backgroundColor}>
      <Container>
        <h2 className="headingWithBar">Lokalteam {localGroup.name}</h2>

        {isExpanded ? (
          <>
            <Markdown>{localGroup.description}</Markdown>
            {image}
          </>
        ) : (
          <Markdown>{localGroup.teaser}</Markdown>
        )}

        <div className={styles.center}>
          <Image
            src={isExpanded ? expandArrowUp : expandArrowDown}
            alt="Zeige mehr über das Lokalteam"

          />
        </div>
      </Container>
    </div>
  );
}
