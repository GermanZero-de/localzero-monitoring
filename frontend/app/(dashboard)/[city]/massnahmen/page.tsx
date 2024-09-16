
import MeasureCard from "@/app/components/MeasureCard";

import Image from "next/image";
import arrow from "@/public/imgs/arrow-right-down.svg";
import { Accordion, Container } from "react-bootstrap";
import styles from "./page.module.scss";
import MeasureCardContent from "@/app/components/MeasureCardContent";

import { ExecutionStatus } from "@/types/enums";
import ExecutionStatusIcon from "@/app/components/ExecutionStatusIcon";
import Markdown from "react-markdown";
import { getCities, getTasks, getRecursiveStatusNumbers } from "@/lib/dataService";
import ImplementationIndicator from "@/app/components/ImplementationIndicator";




export default async function CityMeasures({ params, searchParams }: { params: { city: string}, searchParams:{active:string}  }) {
  const activeKey = searchParams?.active;
  const city = await getCities(params.city);
  const tasks = await getTasks(params.city);
  if (!city || !tasks) {
    return <></>;
  }

  return (
    <Container className={styles.container}>
      <ImplementationIndicator
        style={{height:250, marginBottom:30}}
        tasksNumber={getRecursiveStatusNumbers(tasks)}
        startYear={new Date(city.resolution_date).getFullYear()}
        endYear={city.target_year}
        showLegend
        showNow
      ></ImplementationIndicator>
      <h1 style={{ fontWeight: 600, fontSize: 38 }}>
        {city.name.toUpperCase()}
        <Image
          src={arrow}
          alt=""
        />
      </h1>

      <Markdown className="mdContent">{city.assessment_status}</Markdown>
      <h2 className="headingWithBar">Maßnahmen in {city.name}</h2>
      <Accordion className={styles.accordion} defaultActiveKey={activeKey}>
        {tasks &&
          tasks.map((task:any, i:number) => {
            return (
              <MeasureCard
                key={i}
                eventKey={task.slugs}
                title={task.title}
                statusOfSubTasks={getRecursiveStatusNumbers(task.children)}
              >
                <MeasureCardContent
                  slugs={task.slugs}
                  text={task.teaser}
                  tasks={task.children}
                  eventKey={task.slugs}
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
