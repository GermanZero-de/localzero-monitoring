"use client";

import { useGetCity } from "@/app/CityService";
import { useParams } from "next/navigation";
import { Container } from "react-bootstrap";
import styles from "../page.module.scss";
import Image from "next/image";
import { Task, useGetTasksByCity } from "@/app/TasksService";
import arrow from "../../../../public/images/arrow-right-down.svg";
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
export default function TaskDetails() {
  const params = useParams();
  const { city: citySlug, task: taskSlug } = params;
  const { city, hasError } = useGetCity(citySlug as string);
  const { tasks, hasError: hasErrorinTasks } = useGetTasksByCity(citySlug as string);
  if (!city || hasError || hasErrorinTasks) {
    return <></>;
  }

  const task = tasks && getTaskBySlugs(tasks, taskSlug);
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
