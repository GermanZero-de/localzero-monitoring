import {cookies} from 'next/headers';
import type { Task, StatusCount } from "@/types";
import { ExecutionStatus } from "@/types/enums";

const getCookie = async (name: string) => {
  return cookies().get(name)?.value ?? '';
}

export async function getCities(id: string = "") {
  const sessionid = await getCookie('sessionid');
  const revalidate = sessionid ? 0: 1800;
  const slug = id ? `/${id}` : ""
    const cities = await (await fetch(`${process.env.REST_API || "http://localhost:8000"}/api/cities${slug}?executionStatusCount`, {
      next: { revalidate },
      headers: {
        Accept: "application/json",
        "Content-Type": "application/json;charset=UTF-8",
        Cookie: `sessionid=${sessionid};`
      },
    })).json();
    return cities

}

export async function getTasks(id: string = "") {
  const slug = id ? `/${id}` : ""
  const sessionid = await getCookie('sessionid');
  const revalidate = sessionid ? 0: 1800;
    const tasks = await (await fetch(`${process.env.REST_API || "http://localhost:8000"}/api/cities${slug}/tasks`, {
      next: { revalidate },
      headers: {
        Accept: "application/json",
        "Content-Type": "application/json;charset=UTF-8",
         Cookie: `sessionid=${sessionid};`
      },
    })).json();
    return tasks

}

export const getRecursiveStatusNumbers = (
  tasks: Task[],
): { complete: number; asPlanned: number; delayed: number; failed: number; unknown: number } => {
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
            statusCount.asPlanned++;
            break;
          case ExecutionStatus.COMPLETE:
            statusCount.complete++;
            break;
          case ExecutionStatus.DELAYED:
            statusCount.delayed++;
            break;
          case ExecutionStatus.FAILED:
            statusCount.failed++;
            break;
        }
      }
      return statusCount;
    },
    { complete: 0, asPlanned: 0, delayed: 0, failed: 0, unknown: 0 } as StatusCount,
  );
};