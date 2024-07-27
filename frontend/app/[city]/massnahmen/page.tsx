"use client";

import { useGetCity } from "@/app/CityService";
import Image from "next/image";

import MeasureCard from "@/app/components/MeasureCard";
import { usePathname } from "next/navigation";
import { Accordion, Card, Container } from "react-bootstrap";
import styles from "./page.module.scss";
import abgeschlossen from "../../../public/images/icon-abgeschlossen.svg";
import gescheitert from "../../../public/images/icon-gescheitert.svg";
import inArbeit from "../../../public/images/icon-in_arbeit.svg";
import unbekannt from "../../../public/images/icon-unbekannt.svg";
import verzoegert from "../../../public/images/icon-verzoegert_fehlt.svg";
import MeasureCardContent from "@/app/components/MeasureCardContent";
import { ExecutionStatus, Task, useGetTasksByCity } from "@/app/TasksService";

export default function CityMeasures() {
  const pathname = usePathname();
  const slug = pathname.split("/").at(-2);
  const { city, hasError } = useGetCity(slug);
  const { tasks, hasError: hasErrorinTasks } = useGetTasksByCity(city ? city.id : 1);
  if (!city || hasError || hasErrorinTasks) {
    return <></>;
  }

  const getStatusNumbers = (
    tasks: Task[],
  ): { done: number; inProgress: number; late: number; failed: number; unknown: number } => {
    return tasks.reduce(
      (statusCount, task) => {
        switch (task.execution_status) {
          case ExecutionStatus.UNKNOWN:
            statusCount.unknown++;
            break;
          case ExecutionStatus.AS_PLANNED:
            statusCount.inProgress++;
            break;
          case ExecutionStatus.COMPLETE:
            statusCount.done++;
            break;
          case ExecutionStatus.DELAYED:
            statusCount.late++;
            break;
          case ExecutionStatus.FAILED:
            statusCount.failed++;
            break;
        }
        return statusCount;
      },
      { done: 0, inProgress: 0, late: 0, failed: 0, unknown: 0 },
    );
  };

  return (
    <Container className={styles.container}>
      <h2 className="headingWithBar">Maßnahmen in {city.name}</h2>
      <Accordion
        defaultActiveKey="0"
        className={styles.accordion}
      >
        {tasks &&
          tasks.map((task, i) => {
            return (
              <MeasureCard
                key={i}
                eventKey={i.toString()}
                title={task.title}
                statusOfSubTasks={getStatusNumbers(task.children)}
              >
                <Card.Body>
                  <MeasureCardContent
                    text={task.description}
                    tasks={task.children}
                  ></MeasureCardContent>
                </Card.Body>
              </MeasureCard>
            );
          })}
      </Accordion>
      <div className={styles.legende}>
        <div>
          <Image
            src={abgeschlossen}
            alt="Abgeschlossene Maßnahmen"
          ></Image>
          abgeschlossen
        </div>
        <div>
          <Image
            src={inArbeit}
            alt="Maßnahmen in Arbeit"
          ></Image>
          in Arbeit
        </div>
        <div>
          <Image
            src={verzoegert}
            alt="Verzögerte Maßnahmen"
          ></Image>
          verzögert
        </div>
        <div>
          <Image
            src={gescheitert}
            alt="Gescheiterte Maßnahmen"
          ></Image>
          gescheitert
        </div>
        <div>
          <Image
            src={unbekannt}
            alt="Unbekannte Maßnahmen"
          ></Image>
          unbekannt
        </div>
      </div>
    </Container>
  );
}
