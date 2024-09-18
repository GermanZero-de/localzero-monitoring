import { Task } from "@/types";

export const executionLabels = {
    "complete":"abgeschlossen",
    "asPlanned":"in Arbeit",
    "delayed":"verzögert",
    "failed": "gescheitert",
    "unknown": "unbekannt"
}

interface PreviousNextResult {
  previousItem: Task | undefined;
  currentItem: Task | undefined;
  nextItem: Task | undefined;
  rootItem: Task | undefined;
}


export function findPreviousAndNext(data: Task[], slug: string): PreviousNextResult {
    let currentItem: Task | undefined;
    let previousItem: Task | undefined;
    let nextItem: Task | undefined;
    let rootItem: Task | undefined;


      function traverse(data: Task[], topLevelRoot: Task): void {
        for (let i = 0; i < data.length; i++) {
            const item = data[i];

            if (item.slugs === slug) {
                currentItem = item;
                rootItem = topLevelRoot;
                previousItem = i > 0 ? data[i - 1] : undefined;
                nextItem = i < data.length - 1 ? data[i + 1] : undefined;
                return;
            }

            if (item.children && item.children.length > 0) {
                traverse(item.children, topLevelRoot);
                if (currentItem) return;
            }
        }
    }


    for (const topLevelItem of data) {
        traverse([topLevelItem], topLevelItem);
        if (currentItem) break;
    }

    return { previousItem, currentItem, nextItem, rootItem };
  }

export function flattenTasks(tasks:Task[]) {
    let flatList:Task[] = [];

    function recurse(tasks:Task[]) {
        for (const task of tasks) {
            flatList.push(task); // Add the current task to the flat list
            if (task.children && task.children.length > 0) {
                recurse(task.children); // Recursively process the children
            }
        }
    }

    recurse(tasks); // Start recursion from the top-level tasks
    return flatList;
}