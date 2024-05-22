"use client";

import Image from "next/image";
import Link from "next/link";
import closingIcon from "../../public/x.svg";
import { useState } from "react";
import { db } from "./db/db.server";
import { cpmonitorCity } from "./db/schema";
import { Card, Col, ListGroup, Row } from "react-bootstrap";
import styles from "./Search.module.scss";

export default function Search(props) {
  const [searchTerm, setSearchTerm] = useState("");
  const [filteredCities, setFilteredCities] = useState([]);

  const search = (event) => {
    const newSearchTerm = event.target.value;
    setSearchTerm(newSearchTerm);

    const filteredCities = props.cities.filter((city) => city.name.toLowerCase().includes(newSearchTerm.toLowerCase()));
    setFilteredCities(filteredCities);
  };

  const resetSearch = () => {
    setFilteredCities([]);
    setSearchTerm("");
  };

  return (
    <Row className={styles.background}>
      <Col></Col>
      <Col>
        <div>
          <div className={styles.shadow}>
            <div className={styles.searchMask}>
              <h5 className={styles.searchMaskHeading}>Suche Kommune</h5>
              <div className={styles.inputWrapper}>
                <input
                  value={searchTerm}
                  className={styles.input}
                  type="text"
                  placeholder="Name"
                  onChange={search}
                />
                <Image
                  onClick={resetSearch}
                  src={closingIcon}
                  width={30}
                  height={30}
                  alt="Suche zurücksetzen"
                />
              </div>
            </div>
          </div>
          <ListGroup className={styles.listGroup}>
            {filteredCities.map((city) => (
              <Link
                href={"/" + city.slug + "/"}
                key={city.slug}
              >
                <ListGroup.Item>{city.name}</ListGroup.Item>
              </Link>
            ))}
          </ListGroup>
        </div>
      </Col>
      <Col></Col>
    </Row>
  );
}
