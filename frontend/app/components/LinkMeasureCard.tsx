import React, { useContext } from "react";
import Image from "next/image";
import ArrowRight from "../../public/images/arrow-right.svg";
import { AccordionContext, Card } from "react-bootstrap";
import styles from "./styles/SecondaryMeasureCard.module.scss";

interface LinkMeasureCardProps {
  eventKey: string;
  title: string;
}

const LinkMeasureCard: React.FC<LinkMeasureCardProps> = ({ eventKey, title }) => {
  return (
    <Card>
      <Card.Header className={styles.header}>
        {title}
        <div className={styles.toggle}>
          <Image
            src={ArrowRight}
            alt="Zeige mehr über das Lokalteam"
          />
        </div>
      </Card.Header>
    </Card>
  );
};

export default LinkMeasureCard;
