import * as React from "react";
import styles from "./styles/TaskNavigation.module.scss";
import type { Task } from "@/types";
import Link from "next/link";


type Props = {
    next: string | undefined;
    prev: string | undefined;
    root: string | undefined;
};


const TaskNavigation: React.FC<Props> = ({ next, prev, root }) => {

    return (
        <div className={styles.wrapper}>
            <div></div>

           <Link href={root ?? "./"} className="d-flex flex-column align-items-center">
                <div>Sektorenübersicht</div>
                <div className={`${styles.arrow} ${styles.up}`}></div>
            </Link>
            <div></div>

            {prev ? <Link href={prev ?? "./"} className="d-flex align-items-center">
                <div>vorherige</div>
                <div className={`${styles.arrow} ${styles.left}`}></div>
            </Link> : <div></div>}

            <div className={styles.massnahmen}>Maßnahmen</div>
            <div className="align-content-center" >

            {next ? <Link href={next ?? "./"} className="d-flex align-items-center">
                <div className={`${styles.arrow} ${styles.right}`}></div>
                <div>nächste</div>
            </Link> : <div></div>}

            </div>

        </div>
    );
};

export default TaskNavigation;
