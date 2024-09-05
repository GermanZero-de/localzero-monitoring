import * as React from "react";
import styles from "./styles/TaskSummary.module.scss";
import Image from "next/image";
import arrow from "@/public/imgs/arrow-right.svg";
import ImplementationIndicator from "./ImplementationIndicator";
import indicator from "@/public/imgs/placeholders/indicator.png";
import { ExecutionStatus, TaskStatus } from "@/types/enums";
import type { Task } from "@/types";
import ExecutionStatusIcon from "./ExecutionStatusIcon";
const icons = {
    facebook:
        '<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="28" height="28" viewBox="0 0 28 28"><defs><path id="vsxwc570mb" d="M0 0L11.118 0 11.118 21 0 21z"/></defs><g fill="#011633" fill-rule="evenodd"><g fill="#011633"><g fill="#011633"><g transform="translate(-905 -79) translate(894 68.023) translate(11.5 11.5)"><g transform="translate(7.941 3)"><path fill="#011633" d="M7.216 21v-9.58h3.278l.491-3.732H7.216V5.304c0-1.08.306-1.817 1.886-1.817l2.016-.001V.147C10.769.102 9.573 0 8.18 0 5.275 0 3.286 1.74 3.286 4.935v2.753H0v3.733h3.286V21h3.93z" mask="url(#nlkbp0pfxc)"/></g></g></g></g></g></svg>',
};

type Props = {
    task: Task | undefined;
};

const getStatusLabel = (taskStatus:ExecutionStatus) =>{
    switch (taskStatus) {
        case ExecutionStatus.UNKNOWN:
          return <span style={{color:"#FFA700", fontSize: "1.5em", paddingTop:40}}>unbekannt</span>;
        case ExecutionStatus.AS_PLANNED:
            return <span style={{color:"#FFA700", fontSize: "1.5em", paddingTop:40}}>in Arbeit</span>;
        case ExecutionStatus.COMPLETE:
            return <span style={{color:"#FFA700", fontSize: "1.5em", paddingTop:40}}>abgeschlossen</span>;
        case ExecutionStatus.DELAYED:
            return <span style={{color:"#FFA700", fontSize: "1.5em", paddingTop:40}}>verzögert</span>;
        case ExecutionStatus.FAILED:
            return <span style={{color:"#FFA700", fontSize: "1.5em", paddingTop:40}}>gescheitert</span>;
      }
}

const TaskSummary: React.FC<Props> = ({ task }) => {

    return (
        <div className={styles.wrapper}>

            <div className="py-2 d-flex flex-column">
                <ExecutionStatusIcon taskStatus={task?.execution_status}></ExecutionStatusIcon>
                {getStatusLabel(task?.execution_status)}
                </div>
            <div className={styles.row}>
                <div className={styles.label}>Sektor:</div>
                <div>{task?.root.title}</div>
            </div>
            <div className={styles.row}>
                <div className={styles.label}>Beginn:</div>
                <div>{task?.planned_start}</div>
            </div>
            <div className={styles.row}>
                <div className={styles.label}>Ende:</div>
                <div>{task?.planned_completion}</div>
            </div>
            <div className={styles.row}>
                <div className={styles.label}>Zusständigkeit:</div>
                <div>{task?.responsible_organ}</div>
            </div>
            <div className={styles.row}>
                <div className={styles.label}>Autoren:</div>
                <div></div>
            </div>
            <div className={styles.row}>
                <div className={styles.label}>Kooperation:</div>
                <div>{task?.supporting_ngos}</div>
            </div>
            <div className={styles.row}>
                <div className={styles.label}>Letzte Aktualisierung:</div>
                <div></div>
            </div>
        </div>
    );
};

export default TaskSummary;
