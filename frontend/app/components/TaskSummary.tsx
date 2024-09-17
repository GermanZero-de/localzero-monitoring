import * as React from "react";
import styles from "./styles/TaskSummary.module.scss";
import { ExecutionStatus, TaskStatus } from "@/types/enums";
import type { City, StatusCount, Task } from "@/types";
import ExecutionStatusIcon from "./ExecutionStatusIcon";
import { executionLabels } from "@/lib/utils"
import ImplementationIndicator from "@/app/components/ImplementationIndicator";
import CustomMarkdown from "./CustomMarkdown";

type Props = {
    task: Task | undefined;
    root: Task | undefined;
    city: City;

};

const formatter = new Intl.DateTimeFormat('de')

const getStatusLabel = (taskStatus: ExecutionStatus) => {
    switch (taskStatus) {
        case ExecutionStatus.UNKNOWN:
            return <span style={{ color: "#333333", fontSize: "1.5em", paddingTop: 10 }}>{executionLabels.unknown}</span>;
        case ExecutionStatus.AS_PLANNED:
            return <span style={{ color: "#FFA700", fontSize: "1.5em", paddingTop: 10 }}>{executionLabels.asPlanned}</span>;
        case ExecutionStatus.COMPLETE:
            return <span style={{ color: "#9BD300", fontSize: "1.5em", paddingTop: 10 }}>{executionLabels.complete}</span>;
        case ExecutionStatus.DELAYED:
            return <span style={{ color: "#F65035", fontSize: "1.5em", paddingTop: 10 }}>{executionLabels.delayed}</span>;
        case ExecutionStatus.FAILED:
            return <span style={{ color: "#333333", fontSize: "1.5em", paddingTop: 10 }}>{executionLabels.failed}</span>;
    }
}

const getStatusRow = (attr: string | undefined, title: string, markdown = false, date=false) => {
    if (markdown && attr) {
        return <div className={styles.row}>
            <div className={styles.label}>{title}:</div>
            <div><CustomMarkdown content={attr}></CustomMarkdown></div>
        </div>
    }
    if (date && attr) {
        return <div className={styles.row}>
            <div className={styles.label}>{title}:</div>
            <div>{formatter.format(new Date(attr))}</div>
        </div>
    }
    return attr ? (
        <div className={styles.row}>
            <div className={styles.label}>{title}:</div>
            <div>{attr}</div>
        </div>
    ) : null;
};

const getTaskCounts = (taskStatus: ExecutionStatus): StatusCount => {
    const defaultStatusCount: StatusCount = {
        unknown: 0,
        failed: 0,
        delayed: 0,
        asPlanned: 0,
        complete: 0,
    };

    const statusMap: Partial<Record<ExecutionStatus, keyof StatusCount>> = {
        [ExecutionStatus.UNKNOWN]: "unknown",
        [ExecutionStatus.FAILED]: "failed",
        [ExecutionStatus.DELAYED]: "delayed",
        [ExecutionStatus.AS_PLANNED]: "asPlanned",
        [ExecutionStatus.COMPLETE]: "complete",
    };

    const statusKey = statusMap[taskStatus];
    if (statusKey) {
        defaultStatusCount[statusKey] = 1;
    }

    return defaultStatusCount;
};

const TaskSummary: React.FC<Props> = ({ task, root, city }) => {
    const startYear = task?.planned_start || city.resolution_date;
    const endYear = task?.planned_completion || city?.target_year.toString();
    const indicator = task && startYear && endYear ? <ImplementationIndicator
        style={{ height: 110 }}
        tasksNumber={getTaskCounts(task.execution_status)}
        startYear={new Date(startYear).getFullYear()}
        endYear={new Date(endYear).getFullYear()}
    />
        : <></>
    return (
        <div className={styles.wrapper}>
            {indicator}
            <div className="py-4 d-flex flex-column">
                <ExecutionStatusIcon taskStatus={task?.execution_status}></ExecutionStatusIcon>
                {getStatusLabel(task?.execution_status)}
            </div>
            {getStatusRow(root?.title, "Sektor")}
            {getStatusRow(task?.planned_start, "Beginn", false, true)}
            {getStatusRow(task?.planned_completion, "Ende", false, true)}
            {getStatusRow(task?.responsible_organ, "Zuständigkeit")}
            {getStatusRow(task?.supporting_ngos, "Kooperation", true)}
        </div>
    );
};

export default TaskSummary;
