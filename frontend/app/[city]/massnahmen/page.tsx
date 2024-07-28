"use client";

import { useGetCity } from "@/app/CityService";
import MeasureCard from "@/app/components/MeasureCard";
import { usePathname } from "next/navigation";
import { Accordion, Container } from "react-bootstrap";
import styles from "./page.module.scss";
import MeasureCardContent from "@/app/components/MeasureCardContent";
import { ExecutionStatus, Task, useGetTasksByCity } from "@/app/TasksService";
import ExecutionStatusIcon from "@/app/components/ExecutionStatusIcon";

export type StatusCount = {
  done: number;
  inProgress: number;
  late: number;
  failed: number;
  unknown: number;
};

const getRecursiveStatusNumbers = (
  tasks: Task[],
): { done: number; inProgress: number; late: number; failed: number; unknown: number } => {
  return tasks.reduce(
    (statusCount, task) => {
      if (task.numchild > 0) {
        const childrenStatusNumbers = getRecursiveStatusNumbers(task.children);
        Object.keys(childrenStatusNumbers).forEach((statusKey) => {
          statusCount[statusKey as keyof StatusCount] += childrenStatusNumbers[statusKey as keyof StatusCount];
        });
      } else {
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
      }
      return statusCount;
    },
    { done: 0, inProgress: 0, late: 0, failed: 0, unknown: 0 } as StatusCount,
  );
};

export default function CityMeasures() {
  const pathname = usePathname();
  const slug = pathname.split("/").at(-2);
  const { city, hasError } = useGetCity(slug);
  const { tasks, hasError: hasErrorinTasks } = useGetTasksByCity(city ? city.id : 1);
  if (!city || hasError || hasErrorinTasks) {
    return <></>;
  }

  return (
    <Container className={styles.container}>
      <h2 className="headingWithBar">Maßnahmen in {city.name}</h2>
      <Accordion className={styles.accordion}>
        {tasks &&
          tasks.map((task, i) => {
            return (
              <MeasureCard
                key={i}
                eventKey={i.toString()}
                title={task.title}
                statusOfSubTasks={getRecursiveStatusNumbers(task.children)}
              >
                <MeasureCardContent
                  text={task.description}
                  tasks={task.children}
                  eventKey={i.toString()}
                ></MeasureCardContent>
              </MeasureCard>
            );
          })}
      </Accordion>
      <div className={styles.legende}>
        <div>
          <ExecutionStatusIcon taskStatus={ExecutionStatus.COMPLETE}></ExecutionStatusIcon>
          abgeschlossen
        </div>
        <div>
          <ExecutionStatusIcon taskStatus={ExecutionStatus.AS_PLANNED}></ExecutionStatusIcon>
          in Arbeit
        </div>
        <div>
          <ExecutionStatusIcon taskStatus={ExecutionStatus.DELAYED}></ExecutionStatusIcon>
          verzögert
        </div>
        <div>
          <ExecutionStatusIcon taskStatus={ExecutionStatus.FAILED}></ExecutionStatusIcon>
          gescheitert
        </div>
        <div>
          <ExecutionStatusIcon taskStatus={ExecutionStatus.UNKNOWN}></ExecutionStatusIcon>
          unbekannt
        </div>
      </div>
    </Container>
  );
}
