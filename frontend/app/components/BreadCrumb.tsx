'use client'

import React, { ReactNode } from 'react'

import { usePathname } from 'next/navigation'
import Link from 'next/link'
import styles from "./styles/Breadcrumb.module.scss";

type TBreadCrumbProps = {
}

const Breadcrumb = ({}: TBreadCrumbProps) => {

    const paths = usePathname()
    const pathNames = paths.split('/').filter( path => path )
    const listClasses = "item";
    const activeClasses = "fw-bold";
    return (
        <div>
            <ul className="breadcrumb">
                <li className={`${listClasses} ${styles.item}`}><Link  className={styles.links} href={'/'}>Dashboard</Link></li>
            {
                pathNames.map( (link, index) => {
                    let href = `/${pathNames.slice(0, index + 1).join('/')}`
                    let itemClasses = paths === href ? activeClasses : listClasses
                    let itemLink = link[0].toUpperCase() + link.slice(1, link.length)
                    return (
                        <React.Fragment key={index}>
                            <li className={`${itemClasses} ${styles.links}`} >
                                <Link className={styles.links} href={href}>{itemLink}</Link>
                            </li>
                        </React.Fragment>
                    )
                })
            }
            </ul>
        </div>
    )
}

export default Breadcrumb