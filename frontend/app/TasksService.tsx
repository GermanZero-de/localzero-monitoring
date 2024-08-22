import axios from "axios";
import { useState, useEffect } from "react";

export enum ExecutionStatus {
  UNKNOWN = 0,
  AS_PLANNED = 2,
  COMPLETE = 4,
  DELAYED = 6,
  FAILED = 8,
}

export interface Task {
  id: number;
  title: string;
  description: string;
  execution_status: ExecutionStatus;
  slugs: string;
  numchild: number;
  children: Task[];
  city: number;
}

export function useGetTasksByCity(slug: string): {
  tasks: Task[] | undefined;
  hasError: boolean;
} {
  const [tasks, setTasks] = useState<Task[] | undefined>(undefined);
  const [hasError, setHasError] = useState(false);

  useEffect(() => {
    const getTasksByCity = async () => {
      try {
        const response = await axios.get<Task[]>("http://127.0.0.1:8000/api/cities/" + slug + "/tasks", {
          // TODO: proper url
          headers: {
            Accept: "application/json",
            "Content-Type": "application/json;charset=UTF-8",
          },
        });
        setTasks(response.data);
      } catch (error) {
        console.error("Error get tasks request: ", error);
        setHasError(true);
      }
    };

    getTasksByCity();
  }, [slug]);

  return { tasks, hasError };
}
