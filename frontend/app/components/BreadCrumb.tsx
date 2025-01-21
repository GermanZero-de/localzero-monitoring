'use client'

import React from 'react'
import arrow from "@/public/imgs/arrow-right-down.svg";
import { usePathname } from 'next/navigation'
import Link from 'next/link'
import styles from "./styles/Breadcrumb.module.scss";
import { Col, Container, Row } from 'react-bootstrap';
import Image from "next/image";
import { findPreviousAndNext } from "@/lib/utils";
import { Task } from '@/types';

type TBreadCrumbProps = {
    logo: string
    cityName: string
    tasks: Task[]
}

const Breadcrumb = ({ logo, cityName, tasks }: TBreadCrumbProps) => {

    const paths = usePathname()
    const pathNames = paths.split('/').filter(path => path);
    const listClasses = "item";
    const activeClasses = "fw-bold";
    const labelMapping: { [key: string]: string } = {
        waermeplanung_checkliste: "Wärmeplanung",
        kap_checkliste: "Klimaaktionsplan",
        verwaltungsstrukturen_checkliste: "Verwaltungsstrukturen",
    };
    const localLogo = logo ? <img
        style={{ height: 'auto', objectFit: 'cover', maxWidth: 500, maxHeight: 150 }}
        src={logo}
        alt={"Logo von " + cityName}
    /> : <></>
    return (
        <div style={{ position: "sticky", top: 0, background: "white", zIndex: 11 }}>
            <Container style={{ position: "relative" }}>
                <Row>
                    <Col className="justify-content-between d-md-flex">
                        <h1 style={{ fontWeight: 600, whiteSpace: "nowrap" }} className="mb-0">
                            {cityName}
                            <Image
                                style={{ marginLeft: 10 }}
                                src={arrow}
                                alt=""
                            />
                        </h1>
                    </Col>
                    <Col className="justify-content-end d-md-flex align-self-center">
                        {localLogo}
                    </Col>
                </Row>
                <nav>
                    <ul className="breadcrumb">
                        {
                            pathNames.map((link, index) => {
                                let href = `/${pathNames.slice(0, index + 1).join('/')}`
                                let itemClasses = paths === href ? activeClasses : listClasses
                                let label = labelMapping[link] ?? link[0].toUpperCase() + link.slice(1, link.length)
                                if (index === 0) {
                                    label = "Dashboard"
                                } else {
                                    const token = findPreviousAndNext(tasks, href.split("/").slice(3).join("/"))
                                    if (token?.currentItem) {
                                        label = token.currentItem.title
                                    }
                                }
                                return (
                                    <React.Fragment key={index}>
                                        <li className={`${itemClasses} ${styles.item} ${styles.links}`} >
                                            <Link className={styles.links} href={href}>{label}</Link>
                                        </li>
                                    </React.Fragment>
                                )
                            })
                        }
                    </ul>
                </nav>
            </Container>
        </div>
    )
}

export default Breadcrumb