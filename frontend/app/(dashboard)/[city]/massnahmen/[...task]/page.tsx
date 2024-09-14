
import { findPreviousAndNext, getTasks } from "@/lib/dataService";
import ArrowRight from "@/app/components/icons/ArrowRight";
import { Col, Container, Row } from "react-bootstrap";
import styles from "../page.module.scss";
import { decode } from 'html-entities';
import Markdown from "react-markdown";
import TaskSummary from "@/app/components/TaskSummary";
import TaskNavigation from "@/app/components/TaskNavigation";
import Link from "next/link";

export default async function TaskDetails({ params }: { params: { city: string, task: Array<string> } }) {

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
    <div style={{ width: 250, fontSize: "1.2em" }}>
      <Link href={rootUrl || "./"}>
        <ArrowRight
          color="#40279C"
          style={{ width: 50, transform: "rotate(180deg)", marginRight: 20 }}

        />zurück</Link></div>

  return (
    <Container>
      <Row className="py-5">
        <Col>
          <h2>{task?.title}</h2>
        </Col>
      </Row>
      <Row>
        <Col className="d-flex">
          <div>

            {task.children.length === 0 ? <TaskSummary task={task} root={rootItem}></TaskSummary> : linkback}

          </div>
          <div className="flex-grow-1 px-3 overflow-hidden">
            <div className="d-flex flex-column">
              <h3 className="headingWithBar">Beschreibung</h3>
              <Markdown className={styles.mdContent}>{decode(task?.description)}</Markdown>
            </div>
          </div>
        </Col>
      </Row>
      <Row className="py-5">
        <Col className="justify-content-center">
          {nav}
        </Col>
      </Row>
    </Container>
  );
}
