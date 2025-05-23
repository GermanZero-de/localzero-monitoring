"use client";

import Image from "next/image";
import { Container } from "react-bootstrap";
import Markdown from "react-markdown";
import expandArrowDown from "@/public/imgs/arrow-expand-down.svg";
import expandArrowUp from "@/public/imgs/arrow-expand-up.svg";
import styles from "./styles/LocalGroup.module.scss";
import { LocalGroupType } from "@/types";
import { useState } from "react";
import rehypeRaw from "rehype-raw";
import remarkGfm from 'remark-gfm'

type Props = {
  localGroup: LocalGroupType | null;
  isExpanded: boolean;
};

export default function LocalGroup({ localGroup }: Props) {

  const [isExpanded, setShowAll] = useState(false);

  const toggle = () => {
    setShowAll((prev) => !prev);
  };

  if (!localGroup) {
    return <></>;
  }


  const image = localGroup.featured_image ? (
    <img
      style={{objectFit:"none"}}
      className="pb-3 mw-100"
      src={"./" + localGroup.featured_image}
      alt={"Lokalgruppe " + localGroup.name}
    />
  ) : null;

  return (
    <div className={isExpanded ? styles.fixed : styles.backgroundColor}>
      <Container className="d-flex flex-column">
        <h1 className="headingWithBar">Lokalteam {localGroup.name}</h1>

        {isExpanded ? (
          <>
            <Markdown className="mdContent" rehypePlugins={[rehypeRaw]} remarkPlugins={[remarkGfm]}>{localGroup.description}</Markdown>
            {image}
          </>
        ) : (
          <Markdown className="mdContent" rehypePlugins={[rehypeRaw]} remarkPlugins={[remarkGfm]}>{localGroup.teaser}</Markdown>
        )}

        <div className={styles.center}>
          <Image
            onClick={toggle}
            src={isExpanded ? expandArrowUp : expandArrowDown}
            title="Zeige mehr über das Lokalteam"
            alt="Zeige mehr über das Lokalteam"
            style={{ cursor: "pointer" }}
          />
        </div>
      </Container>
    </div>
  );
}