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
  website: string;
  featuredImage: string;
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
        <Markdown>{localGroup.teaser}</Markdown>

        {isExpanded ? <Markdown>{localGroup.description}</Markdown> : <div></div>}

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
