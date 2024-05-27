"use client";

import Image from "next/image";
import { Container } from "react-bootstrap";
import Markdown from "react-markdown";
import expandArrowDown from "../../public/images/arrow-expand-down.svg";
import expandArrowUp from "../../public/images/arrow-expand-up.svg";
import styles from "./styles/LocalGroup.module.scss";

type Props = {
  localGroup: LocalGroupType;
  isExpanded: boolean;
  setIsExpanded: (isExpanded: boolean) => void;
};

type LocalGroupType = {
  name: string;
  teaser: string;
  featured_image: string;
  description: string;
};

export default function LocalGroup({ localGroup, isExpanded, setIsExpanded }: Props) {
  if (!localGroup) {
    return <></>;
  }

  return (
    <div className={isExpanded ? styles.fixed : styles.backgroundColor}>
      <Container>
        <h2>Lokalteam {localGroup.name}</h2>

        {isExpanded ? (
          <>
            <Markdown>{localGroup.description}</Markdown>
            <img
              className="pb-3"
              src={"http://127.0.0.1:8000" + localGroup.featured_image}
              alt={"Lokalgruppe " + localGroup.name}
            ></img>
          </>
        ) : (
          <Markdown>{localGroup.teaser}</Markdown>
        )}

        <div className={styles.center}>
          <Image
            src={isExpanded ? expandArrowUp : expandArrowDown}
            alt="Zeige mehr über das Lokalteam"
            onClick={() => setIsExpanded(!isExpanded)}
          />
        </div>
      </Container>
    </div>
  );
}
