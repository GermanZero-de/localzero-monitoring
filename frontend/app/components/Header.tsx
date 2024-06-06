"use client";
import { Container, Navbar, Nav, NavDropdown } from "react-bootstrap";
import Image from 'next/image'
import logo from '../../public/logo.png'
import spende from '../../public/spende.svg'

export default function Header() {
  return (
    <Navbar
      color="light"
      expand="lg"
      className="border-bottom border-gray bg-white"
    >
      <Container>
        <Navbar.Brand href="/">
          {" "}
          <Image
            src={logo}
            width={200}
            className="d-inline-block align-top"
            alt="LocalZero Monitoring logo"
          />
        </Navbar.Brand>
        <Navbar.Toggle aria-controls="basic-navbar-nav" />
        <Navbar.Collapse id="basic-navbar-nav">
          <Nav className="fw-bold m-auto">
            <NavDropdown title="MONITORING">
              <NavDropdown.Item href="/">START</NavDropdown.Item>
              <NavDropdown.Item href="projektbeschreibung">PROJEKTBESCHREIBUNG</NavDropdown.Item>
              <NavDropdown.Item href="mitmachen">MITMACHEN</NavDropdown.Item>
              <NavDropdown.Item href="kontakt">KONTAKT</NavDropdown.Item>
              <NavDropdown.Item href="impressum">IMPRESSUM</NavDropdown.Item>
              <NavDropdown.Item href="datenschutz">DATENSCHUTZ</NavDropdown.Item>
            </NavDropdown>

            <Nav.Link href="#suche_kommune">SUCHE KOMMUNE</Nav.Link>
            <Nav.Link href="topmassnahmen">TOP MASSNAHMEN</Nav.Link>
          </Nav>

        <Navbar.Brand href="#home">
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
