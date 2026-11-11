"use client";
import { useState } from "react";
import { Container, Navbar, Nav, NavDropdown } from "react-bootstrap";
import Image from "next/image";
import logo from "@/public/logo.png";
import spende from "@/public/spende.svg";
import arrow from "@/public/imgs/arrow-right-down.svg";

export default function Header() {
  const [showDropdown, setShowDropdown] = useState(false);

  return (
    <Navbar
      color="light"
      expand="lg"
      className="bg-white py-3"
    >
      <Container>
        <Navbar.Brand href="/">
          <Image
            src={logo}
            width={180}
            className="d-inline-block align-top"
            alt="LocalZero Monitoring logo"
          />
        </Navbar.Brand>
        <Navbar.Toggle aria-controls="basic-navbar-nav" />
        <Navbar.Collapse id="basic-navbar-nav">
          <Nav
            fill
            className="fw-bold flex-grow-1"
          >
            <Nav.Link href="/">ALLE KOMMUNEN</Nav.Link>
            <Nav.Link href="/projektbeschreibung">ÜBER DAS PROJEKT</Nav.Link>

            <Nav.Link
              href="https://localzero.net/loesungen/top-massnahmen"
              target="_blank"
              aria-label="Öffne das Germanzero Wiki in neuem Tab"
            >
              TOP MASSNAHMEN
            </Nav.Link>
          </Nav>

          <Navbar.Brand
            href="https://localzero.net/jetzt-spenden"
            target="new"
          >
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
