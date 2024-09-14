"use client";

import Image from "next/image";
import Link from "next/link";
import closingIcon from "@/public/x.svg";
import { useState } from "react";
import {  Col, ListGroup, Row } from "react-bootstrap";
import styles from "./Search.module.scss";
import { City } from "@/types";

interface SearchResult {
  name: string;
  slug: string;
}

interface SearchProps {
  cities: SearchResult[];
}

export default function Search(props:SearchProps) {
  const [searchTerm, setSearchTerm] = useState<string>("");
  const [filteredCities, setFilteredCities] = useState<SearchResult[]>([]);

  const search = (event:React.ChangeEvent<HTMLInputElement>) => {
    const newSearchTerm = event.target.value;
    setSearchTerm(newSearchTerm);

    const filteredCities = props.cities.filter((city:SearchResult) => city.name.toLowerCase().includes(newSearchTerm.toLowerCase()));
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
              <h5 className={styles.searchMaskHeading} id="suche_kommune">Suche Kommune</h5>
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
            {filteredCities.map((city:SearchResult) => (
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
