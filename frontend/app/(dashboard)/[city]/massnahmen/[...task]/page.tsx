
import { getCities, getTasks } from "@/lib/dataService";
import Image from "next/image";
import indicator from "@/public/imgs/placeholders/indicator.png";
import { Col, Container, Row } from "react-bootstrap";
import styles from "../page.module.scss";
import type { Task } from "@/types";
import Markdown from "react-markdown";
import TaskSummary from "@/app/components/TaskSummary";

const getTaskBySlug = (tasks: Task[] | undefined, taskSlug: string): Task | undefined => {
  return tasks?.find((task) => task.slugs.includes(taskSlug));
};

const getTaskBySlugs = (tasks: Task[] | undefined, taskSlugs: string | string[]): Task | undefined => {
  if (typeof taskSlugs === "string") {
    return getTaskBySlug(tasks, taskSlugs);
  } else if (Array.isArray(taskSlugs)) {
    // avoid mutaion of the original slug object
    taskSlugs = [...taskSlugs];
    const taskGroup = getTaskBySlug(tasks, taskSlugs[0]);
    const childSlug = taskSlugs[0] + "/" + taskSlugs[1];
    taskSlugs.splice(0, 2, childSlug);
    if (taskSlugs.length == 1) {
      taskSlugs = taskSlugs[0];
    }
    return getTaskBySlugs(taskGroup?.children, taskSlugs);
  }
};
export default async function TaskDetails({ params }: { params: { city: string, task: string } }) {

  const tasks = await getTasks(params.city)


  if (!tasks) {
    return <h3 className="pb-3 pt-3">Für die Stadt {params.city} gibt es kein Monitoring</h3>;
  }

  const task = getTaskBySlugs(tasks, params.task);
  const rootTaskSlug = task?.slugs.split("/")[0];
  const flatTaskList = tasks.flat(10)

  if (!task) {
    return <h3 className="pb-3 pt-3">Für die Stadt {params.city} gibt es kein Monitoring</h3>;
  }

  task.root = flatTaskList.find((t:Task)=>t.slugs===rootTaskSlug);

  return (
    <Container>
      <Row className="py-5">
        <Col>
          <h2>{task?.title}</h2>
        </Col>
      </Row>
      <Row>
        <Col  className="d-flex">
          <div>
            <Image
              width={250}
              src={indicator}
              alt={"Fortschritt zur Klimaneutralität"}
            />
            <TaskSummary task={task}></TaskSummary>
          </div>
          <div className="flex-grow-1 px-3 overflow-hidden">
            <div className="d-flex flex-column">
              <h3 className="headingWithBar">Beschreibung</h3>
              <Markdown className={styles.mdContent}>{task?.description}</Markdown>
            </div>
          </div>
        </Col>
      </Row>
    </Container>
  );
}
