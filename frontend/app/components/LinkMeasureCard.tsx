"use client"

import React from "react";
import Image from "next/image";
import ArrowRight from "@/public/imgs/arrow-right.svg";
import { Card } from "react-bootstrap";
import styles from "./styles/SecondaryMeasureCard.module.scss";
import { usePathname, useRouter } from "next/navigation";
import { ExecutionStatus, TaskSource } from "@/types/enums";
import ExecutionStatusIcon from "./ExecutionStatusIcon";

interface LinkMeasureCardProps {
  title: string;
  slugs: string;
  taskStatus: ExecutionStatus;
  source: TaskSource
}

const LinkMeasureCard: React.FC<LinkMeasureCardProps> = ({ title, slugs, taskStatus, source }) => {
  const router = useRouter();
  const currentPath = usePathname();

  const suggested =   source === TaskSource.suggested ? <div className={styles.suggested}></div> : <></>
  return (
    <Card className={styles.closedcard}>
         {suggested}
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
