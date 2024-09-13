import * as React from "react";
import styles from "./styles/TaskSummary.module.scss";
import { ExecutionStatus } from "@/types/enums";
import type { Task } from "@/types";
import ExecutionStatusIcon from "./ExecutionStatusIcon";

import Image from "next/image";
import indicator from "@/public/imgs/placeholders/indicator.png";

type Props = {
    task: Task | undefined;
    root: Task | undefined;
};

const getStatusLabel = (taskStatus:ExecutionStatus) =>{
    switch (taskStatus) {
        case ExecutionStatus.UNKNOWN:
          return <span style={{color:"#333333", fontSize: "1.5em", paddingTop:10}}>unbekannt</span>;
        case ExecutionStatus.AS_PLANNED:
            return <span style={{color:"#FFA700", fontSize: "1.5em", paddingTop:10}}>in Arbeit</span>;
        case ExecutionStatus.COMPLETE:
            return <span style={{color:"#9BD300", fontSize: "1.5em", paddingTop:10}}>abgeschlossen</span>;
        case ExecutionStatus.DELAYED:
            return <span style={{color:"#F65035", fontSize: "1.5em", paddingTop:10}}>verzögert</span>;
        case ExecutionStatus.FAILED:
            return <span style={{color:"#333333", fontSize: "1.5em", paddingTop:10}}>gescheitert</span>;
      }
}

const getStatusRow = (attr: string | undefined, title: string) => {
    return attr ? (
        <div className={styles.row}>
            <div className={styles.label}>{title}:</div>
            <div>{attr}</div>
        </div>
    ) : null;
};
const TaskSummary: React.FC<Props> = ({ task, root }) => {

    return (
        <div className={styles.wrapper}>
            <Image
              width={250}
              src={indicator}
              alt={"Fortschritt zur Klimaneutralität"}
            />
            <div className="py-4 d-flex flex-column">
                <ExecutionStatusIcon taskStatus={task?.execution_status}></ExecutionStatusIcon>
                {getStatusLabel(task?.execution_status)}
                </div>
            {getStatusRow(root?.title, "Sektor")}
            {getStatusRow(task?.planned_start, "Beginn")}
            {getStatusRow(task?.planned_completion, "Ende")}
            {getStatusRow(task?.responsible_organ, "Zusständigkeit")}
            {getStatusRow(task?.supporting_ngos, "Kooperation")}
        </div>
    );
};

export default TaskSummary;
