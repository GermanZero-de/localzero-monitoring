'use client'

import * as React from "react";
import styles from "./styles/TaskNavigation.module.scss";
import Link from "next/link";
import Offcanvas from 'react-bootstrap/Offcanvas';
import TaskTreeView from "@/app/components/TaskTreeView";
import { Task } from "@/types";

type Props = {
    next: string | undefined;
    prev: string | undefined;
    root: string | undefined;
    tasks: Task[];
    baseUrl?:string;
    active?:string;
    cityname: string;
};


const TaskNavigation: React.FC<Props> = ({ next, prev, root, tasks, baseUrl, active, cityname }) => {
    const [show, setShow] = React.useState(false);

    const handleClose = () => setShow(false);
    const handleShow = () => setShow(true);
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

            <div className={styles.massnahmen} onClick={handleShow}>Maßnahmen</div>
            <div className="align-content-center" >

            {next ? <Link href={next ?? "./"} className="d-flex align-items-center">
                <div className={`${styles.arrow} ${styles.right}`}></div>
                <div>nächste</div>
            </Link> : <div></div>}

            </div>

            <Offcanvas show={show} onHide={handleClose} placement="end" className="custom-offcanvas">
                <Offcanvas.Header closeButton>
                <Offcanvas.Title>Maßnahmen in {cityname}</Offcanvas.Title>
                </Offcanvas.Header>
                <Offcanvas.Body>
                <TaskTreeView tasks={tasks} baseUrl={baseUrl} active={active}/>
                </Offcanvas.Body>
            </Offcanvas>
        </div>
    );
};

export default TaskNavigation;
