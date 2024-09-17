
import { findPreviousAndNext, getCities, getTasks } from "@/lib/dataService";
import ArrowRight from "@/app/components/icons/ArrowRight";
import { Col, Container, Row, Tooltip } from "react-bootstrap";
import styles from "./page.module.scss";
import Image from "next/image";
import TaskSummary from "@/app/components/TaskSummary";
import TaskNavigation from "@/app/components/TaskNavigation";
import Link from "next/link";
import localZero from "@/public/imgs/localZero.svg";
import rehypeRaw from "rehype-raw";
import CustomMarkdown from "@/app/components/CustomMarkdown";

export default async function TaskDetails({ params }: { params: { city: string, task: Array<string> } }) {

  const city = await getCities(params.city)
  const tasks = await getTasks(params.city)


  if (!tasks) {
    return <h3 className="pb-3 pt-3">Für die Stadt {params.city} gibt es kein Monitoring</h3>;
  }


  const currentSlug = params.task.join("/")
  const { previousItem, currentItem, nextItem, rootItem } = findPreviousAndNext(tasks, currentSlug);

  const task = currentItem;

  const rootTaskSlug = task?.slugs.split("/")[0];


  if (!task) {
    return <h3 className="pb-3 pt-3">Maßnahme {task} wurde nicht gefunden</h3>;
  }





  const nextUrl = nextItem ? `/${params.city}/massnahmen/${nextItem?.slugs}` : undefined;
  const prevUrl = previousItem ? `/${params.city}/massnahmen/${previousItem?.slugs}` : undefined;
  const rootUrl = rootItem ? `/${params.city}/massnahmen/?active=${rootTaskSlug}#${rootTaskSlug}` : undefined;

  const nav = task.children.length === 0 ? <TaskNavigation prev={prevUrl} next={nextUrl} root={rootUrl}></TaskNavigation> : <></>

  const linkback =
    <div style={{ width: 250, fontSize: "1.2em", position: "sticky", top: "100px" }}>
      <Link href={rootUrl || "./"}>
        <ArrowRight
          color="#40279C"
          style={{ width: 50, transform: "rotate(180deg)", marginRight: 20 }}

        />zurück</Link></div>

  const topmapNahme = task.source === 1 ? <>
    <div className={styles.cornerTop}>
      <Image
        src={localZero}
        alt="LocalZero Top Maßnahme"
        title="LocalZero Maßnahme: Diese Maßnahme ist vom Netzwerk LocalZero oder dem Lokalteam vorgeschlagen.Die Kommune hat sie bisher nicht geplant. Sie ist aber dringend notwendig auf dem Weg zur Klimaneutralität. Sie ist einfach umzusetzen und/oder spart schnell und viel Treibhausgase ein."

      />
    </div>

      <div className={styles.cornerBottom}>
        <Image
          title="LocalZero Maßnahme: Diese Maßnahme ist vom Netzwerk LocalZero oder dem Lokalteam vorgeschlagen.Die Kommune hat sie bisher nicht geplant. Sie ist aber dringend notwendig auf dem Weg zur Klimaneutralität. Sie ist einfach umzusetzen und/oder spart schnell und viel Treibhausgase ein."
          src={localZero}
          alt="LocalZero Top Maßnahme"
        />

      </div></> : <></>

      const assestment = task.plan_assessment ? <><h1 className="headingWithBar">Bewertung der geplanten Maßnahme</h1><CustomMarkdown content={task?.plan_assessment}></CustomMarkdown></> : <></>
      const execution = task.execution_justification ? <><h1 className="headingWithBar">Begründung Umsetzungsstand</h1><CustomMarkdown content={task?.execution_justification}></CustomMarkdown></> : <></>
      const explanation = task.responsible_organ_explanation ? <><h1 className="headingWithBar">Zuständige Instanz</h1><CustomMarkdown content={task?.responsible_organ_explanation}></CustomMarkdown></> : <></>
      const supporting_ngos = task.supporting_ngos ? <><h1 className="headingWithBar">Mit Unterstützung von</h1><CustomMarkdown content={task?.supporting_ngos}></CustomMarkdown></> : <></>


  return (
    <Container className={`${styles.container} ${task.source === 1 ? styles.top : ""}`}>
      <Row>
        <Col>
          <h1>{task?.title}</h1>
          {topmapNahme}
        </Col>
      </Row>
      <Row>
        <Col className="d-flex">
          <div>

            {task.children.length === 0 ? <TaskSummary task={task} root={rootItem} city={city}></TaskSummary> : linkback}

          </div>
          <div className="flex-grow-1 px-3 overflow-hidden">
            <div className="d-flex flex-column">

              <CustomMarkdown className={styles.teaserContent} content={task?.teaser}></CustomMarkdown>
              <h1 className="headingWithBar">Beschreibung</h1>
              <CustomMarkdown  content={task?.description}></CustomMarkdown>

              {assestment}
              {execution}
              {explanation}
              {supporting_ngos}
            </div>
          </div>
        </Col>
      </Row>
      <Row className="py-5">
        <Col className="justify-content-center">
          {nav}

        </Col>
      </Row>
    </Container >
  );
}
