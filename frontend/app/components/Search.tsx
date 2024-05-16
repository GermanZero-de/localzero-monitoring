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
      city.name.toLowerCase().startsWith(searchTerm.toLowerCase()),
    );
    setFilteredCities(filteredCities);
  };

  return (
    <Row className={styles.background}>
      <Col></Col>
      <Col>
        <Card className={styles.card}>
          <Card.Body>
            <Card.Title>Suche Kommune</Card.Title>
            <Card.Text>
              <input
                className={styles.input}
                type="text"
                placeholder="Name"
                onChange={search}
              />
              <ListGroup>
                {filteredCities.map((city) => (
                  <ListGroup.Item className={styles.listItem} key={city.name}>{city.name}</ListGroup.Item>
                ))}
              </ListGroup>
            </Card.Text>
          </Card.Body>
        </Card>
      </Col>
      <Col></Col>
    </Row>
  );
}
