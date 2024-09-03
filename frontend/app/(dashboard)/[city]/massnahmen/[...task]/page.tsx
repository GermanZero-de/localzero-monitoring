
import { getCities, getTasks } from "@/lib/dataService";

import { Container } from "react-bootstrap";
import styles from "../page.module.scss";
import Image from "next/image";
import type { Task } from "@/types";
import arrow from "@/public/imgs/arrow-right-down.svg";
import Breadcrumb from "@/app/components/BreadCrumb";

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

  const city = await getCities(params.city);
  const tasks = await getTasks(params.city)

  if (!city || !tasks) {
    return <h3 className="pb-3 pt-3">Für die Stadt {params.city} gibt es kein Monitoring</h3>;
  }

  const task = getTaskBySlugs(tasks, params.task);
  return (
    <Container className={styles.container}>
      <h1 style={{ fontWeight: 600, fontSize: 38 }}>
        {city.name.toUpperCase()}
        <Image
          src={arrow}
          alt=""
        />
      </h1>
      <Breadcrumb />
      <h2 className="headingWithBar">{task?.title}</h2>
    </Container>
  );
}
