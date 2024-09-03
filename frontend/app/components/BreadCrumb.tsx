'use client'

import React, { ReactNode } from 'react'
import arrow from "@/public/imgs/arrow-right-down.svg";
import { usePathname } from 'next/navigation'
import Link from 'next/link'
import styles from "./styles/Breadcrumb.module.scss";
import { Container } from 'react-bootstrap';
import Image from "next/image";

const Breadcrumb = () => {

    const paths = usePathname()
    const pathNames = paths.split('/').filter(path => path);

    const citySlug = pathNames[0] ?? "";
    const cityName = citySlug[0]?.toUpperCase() + citySlug?.slice(1)

    const listClasses = "item";
    const activeClasses = "fw-bold";
    return (
        <div>
            <Container>
                <h1 style={{ fontWeight: 600, fontSize: 38 }}>
                    {cityName}
                    <Image
                        src={arrow}
                        alt=""
                    />
                </h1>

                <ul className="breadcrumb">
                    <li className={`${listClasses} ${styles.item}`}><Link className={styles.links} href={'/'}>Dashboard</Link></li>
                    {
                        pathNames.map((link, index) => {
                            let href = `/${pathNames.slice(0, index + 1).join('/')}`
                            let itemClasses = paths === href ? activeClasses : listClasses
                            let itemLink = link[0].toUpperCase() + link.slice(1, link.length)
                            return (
                                <React.Fragment key={index}>
                                    <li className={`${itemClasses} ${styles.item} ${styles.links}`} >
                                        <Link className={styles.links} href={href}>{itemLink}</Link>
                                    </li>
                                </React.Fragment>
                            )
                        })
                    }
                </ul>
            </Container>
        </div>
    )
}

export default Breadcrumb