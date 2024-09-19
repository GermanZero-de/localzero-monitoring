"use client";
import { useState } from 'react';
import { Container, Navbar, Nav, NavDropdown } from "react-bootstrap";
import Image from "next/image";
import logo from "@/public/logo.png";
import spende from "@/public/spende.svg";

export default function Header() {
  const [showDropdown, setShowDropdown] = useState(false);

  return (
    <Navbar
      color="light"
      expand="lg"
      className="border-bottom border-gray bg-white"
    >
      <Container>
        <Navbar.Brand href="/">
          <Image
            src={logo}
            width={200}
            className="d-inline-block align-top"
            alt="LocalZero Monitoring logo"
          />
        </Navbar.Brand>
        <Navbar.Toggle aria-controls="basic-navbar-nav" />
        <Navbar.Collapse id="basic-navbar-nav">
          <Nav fill className="fw-bold flex-grow-1">
            <NavDropdown
              title="MONITORING"
              show={showDropdown}
              onMouseEnter={() => setShowDropdown(true)}
              onMouseLeave={() => setShowDropdown(false)}
              onClick={() => setShowDropdown(!showDropdown)}
            >
              <div className="dropDownDivider"></div>
              <NavDropdown.Item href="/">ALLE KOMMUNEN</NavDropdown.Item>
              <NavDropdown.Item href="/projektbeschreibung">ÜBER DAS PROJEKT</NavDropdown.Item>
            </NavDropdown>

            <Nav.Link href="#suche_kommune">SUCHE KOMMUNE</Nav.Link>
            <Nav.Link href="/topmassnahmen">TOP MASSNAHMEN</Nav.Link>
          </Nav>

          <Navbar.Brand href="https://localzero.net/jetzt-spenden" target="new">
            <Image
              src={spende}
              width={200}
              className="d-inline-block align-top"
              alt="Spenden"
            />
          </Navbar.Brand>
        </Navbar.Collapse>
      </Container>
    </Navbar>
  );
}
