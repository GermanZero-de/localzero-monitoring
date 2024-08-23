"use client"

import React from "react";
import Image from "next/image";
import ArrowRight from "../../public/images/arrow-right.svg";
import { Card } from "react-bootstrap";
import styles from "./styles/SecondaryMeasureCard.module.scss";
import { usePathname, useRouter } from "next/navigation";
import { ExecutionStatus } from "../TasksService";
import ExecutionStatusIcon from "./ExecutionStatusIcon";

interface LinkMeasureCardProps {
  title: string;
  slugs: string;
  taskStatus: ExecutionStatus;
}

const LinkMeasureCard: React.FC<LinkMeasureCardProps> = ({ title, slugs, taskStatus }) => {
  const router = useRouter();
  const currentPath = usePathname();
  return (
    <Card className={styles.closedcard}>
      <Card.Header
        className={styles.header}
        onClick={() => router.push(currentPath + "/" + slugs + "/")}
      >
        <ExecutionStatusIcon taskStatus={taskStatus}></ExecutionStatusIcon>
        {title}
        <div className={styles.toggle}>
          <Image
            src={ArrowRight}
            alt="Zeige mehr über die Massnahme"
          />
        </div>
      </Card.Header>
    </Card>
  );
};

export default LinkMeasureCard;
