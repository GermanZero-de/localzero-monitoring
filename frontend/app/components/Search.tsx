"use client";

import { useState } from "react";
import { db } from "./db/db.server";
import { cpmonitorCity } from "./db/schema";
import { Card, Col, ListGroup, Row } from "react-bootstrap";
import styles from "./Search.module.scss";

export default function Search(props) {
  const [filteredCities, setFilteredCities] = useState([]);

  const search = (event) => {
    const searchTerm = event.target.value;

    const filteredCities = props.cities.filter((city) =>
      city.name.toLowerCase().includes(searchTerm.toLowerCase()),
    );
    setFilteredCities(filteredCities);
  };

  return (
    <Row className={styles.background}>
      <Col></Col>
      <Col>
        <div>
          <div className={styles.searchMask}>
            <h5 className={styles.searchMaskHeading}>Suche Kommune</h5>
            <input
              className={styles.input}
              type="text"
              placeholder="Name"
              onChange={search}
            />
          </div>
          <ListGroup className={styles.listGroup}>
            {filteredCities.map((city) => (
              <Link href={"/" + city.slug + "/"} key={city.slug}>
                <ListGroup.Item className={styles.listItem}>{city.name}</ListGroup.Item>
              </Link>
            ))}
          </ListGroup>
        </div>
      </Col>
      <Col></Col>
    </Row>
  );
}
